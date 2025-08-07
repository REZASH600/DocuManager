from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.documents.models import DocumentCategory


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


