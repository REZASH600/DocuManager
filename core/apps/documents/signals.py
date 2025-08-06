
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import DocumentCategory, UploadedTextFile, DocumentType, Document


@receiver(pre_save, sender=DocumentCategory)
def soft_delete_related_types_and_documents_and_text_files(sender, instance, **kwargs):
    """
    If DocumentCategory is being soft-deleted (is_deleted=True),
    also soft-delete all related DocumentTypes and their Documents and UploadTextFile.
    """
    if not instance.pk:
        # New object; no soft-delete needed
        return

    try:
        previous = DocumentCategory.objects.get(pk=instance.pk)
    except DocumentCategory.DoesNotExist:
        return

    if not previous.is_deleted and instance.is_deleted:
        # Soft-delete all related DocumentTypes and their Documents
        DocumentType.objects.filter(category=instance, is_deleted=False).update(
            is_deleted=True
        )

        Document.objects.filter(document_type__category=instance, is_deleted=False).update(is_deleted=True)

        UploadedTextFile.objects.filter(document_type__category=instance).delete()






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
        has_active = Document.objects.filter(
            document_type=instance.document_type,
            is_active=True
        ).exclude(pk=instance.pk).exists()

        if not has_active:
            instance.is_active = True