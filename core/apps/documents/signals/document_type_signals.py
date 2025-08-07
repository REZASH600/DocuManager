from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.documents.models import DocumentType, Document, UploadedTextFile
from apps.documents.utils.document_helpers import (
    should_extract_text_for_type,
    extract_pdf_text,
)


@receiver(pre_save, sender=DocumentType)
def pre_save_document_type(sender, instance, **kwargs):
    """
    Before saving a DocumentType:
    - If soft-deleted or deactivated or visibility is fully disabled,
      then delete all related UploadedTextFiles.
    - If re-activated or visibility re-enabled, mark it for text extraction after save.
    """
    if not instance.pk:
        return  # New object, no action needed

    try:
        previous = DocumentType.objects.get(pk=instance.pk)
    except DocumentType.DoesNotExist:
        return

    should_delete_uploaded_texts = False

    # Soft-delete: also soft-delete related Documents
    if not previous.is_deleted and instance.is_deleted:
        should_delete_uploaded_texts = True
        Document.objects.filter(document_type=instance).update(is_deleted=True)

    # Deactivation
    if previous.is_active and not instance.is_active:
        should_delete_uploaded_texts = True

    # Both visibilities disabled
    if (previous.private_visible or previous.public_visible) and (
        not instance.private_visible and not instance.public_visible
    ):
        should_delete_uploaded_texts = True

    # Perform deletion of related text files if needed
    if should_delete_uploaded_texts:
        UploadedTextFile.objects.filter(document_type=instance).delete()

    # If re-activated or visibility enabled → mark for post-save text extraction
    reactivated = not previous.is_active and instance.is_active
    visibility_enabled = not (previous.private_visible or previous.public_visible) and (
        instance.private_visible or instance.public_visible
    )

    if (reactivated or visibility_enabled) and should_extract_text_for_type(instance):
        instance._should_extract_texts = True


@receiver(post_save, sender=DocumentType)
def post_save_document_type(sender, instance, **kwargs):
    """
    After saving a DocumentType:
    - If marked for extraction, extract text from all related active & non-deleted Documents
      that don’t already have UploadedTextFiles.
    """
    if getattr(instance, "_should_extract_texts", False):
        documents = Document.objects.filter(
            document_type=instance, is_active=True, is_deleted=False
        ).exclude(uploaded_texts__isnull=False)

        for doc in documents:
            file_path = doc.file.path
            text = extract_pdf_text(file_path)
            if text:
                UploadedTextFile.objects.create(
                    text=text, document=doc, document_type=instance
                )
