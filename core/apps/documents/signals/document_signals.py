from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.documents.models import Document, UploadedTextFile
from apps.documents.utils.document_helpers import should_extract_text_for_document
from apps.documents.tasks.extract_text import extract_text_from_document


@receiver(pre_save, sender=Document)
def ensure_single_active_document_per_type(sender, instance, **kwargs):
    """
    Ensure only one active Document per DocumentType.
    """
    if instance.is_deleted:
        return  # Ignore deleted documents

    if instance.is_active:
        Document.objects.filter(
            document_type=instance.document_type,
            is_active=True,
        ).exclude(pk=instance.pk).update(is_active=False)
    else:
        has_active = (
            Document.objects.filter(
                document_type=instance.document_type, is_active=True
            )
            .exclude(pk=instance.pk)
            .exists()
        )

        if not has_active:
            instance.is_active = True


@receiver(pre_save, sender=Document)
def pre_save_document(sender, instance, **kwargs):
    """
    Before saving a Document:
    - If it's being soft-deleted or deactivated, delete all related UploadedTextFile(s).
    - If it's being re-activated, mark it for text extraction in post_save.
    """
    if not instance.pk:
        return  # New object — handled in post_save

    try:
        previous = Document.objects.get(pk=instance.pk)
    except Document.DoesNotExist:
        return

    # Case: Document is being soft-deleted or deactivated
    if (not previous.is_deleted and instance.is_deleted) or (
        previous.is_active and not instance.is_active
    ):
        UploadedTextFile.objects.filter(document=instance).delete()

    # Case: Document is being re-activated
    if not previous.is_active and instance.is_active:
        if should_extract_text_for_document(instance):
            instance._should_extract_text = True


@receiver(post_save, sender=Document)
def post_save_document(sender, instance, created, **kwargs):
    """
    After saving a Document:
    - If it’s newly created or marked for extraction in pre_save,
      extract PDF text and create UploadedTextFile.
    """
    if created or getattr(instance, "_should_extract_text", False):
        if should_extract_text_for_document(instance):
            extract_text_from_document.delay(instance.pk)
