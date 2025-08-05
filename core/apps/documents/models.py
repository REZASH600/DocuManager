from django.db import models

from django.utils.translation import gettext_lazy as _

from apps.participants.models import Participant
from .validations import validate_pdf_file


class DocumentCategory(models.Model):
    company_id = models.IntegerField(verbose_name=_("Company ID"))
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="document_categories",
        verbose_name=_("Participant"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Is Deleted"))

    class Meta:
        verbose_name = _("Document Category")
        verbose_name_plural = _("Document Categories")

    def __str__(self):
        return self.title


class DocumentType(models.Model):
    category = models.ForeignKey(
        DocumentCategory,
        on_delete=models.CASCADE,
        related_name="document_types",
        verbose_name=_("Category"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    private_visible = models.BooleanField(
        default=False, verbose_name=_("Private Visible")
    )
    public_visible = models.BooleanField(
        default=False, verbose_name=_("Public Visible")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Is Deleted"))

    class Meta:
        verbose_name = _("Document Type")
        verbose_name_plural = _("Document Types")

    def __str__(self):
        return self.title


class Document(models.Model):
    company_id = models.IntegerField(verbose_name=_("Company ID"))
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Participant"),
    )
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Document Type"),
    )
    file = models.FileField(
        upload_to="documents/", verbose_name=_("File"), validators=[validate_pdf_file]
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Is Deleted"))

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")


class UploadedTextFile(models.Model):
    text = models.TextField(verbose_name=_("Text"))
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name="uploaded_texts",
        verbose_name=_("Document Type"),
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="uploaded_texts",
        verbose_name=_("Document"),
    )

    class Meta:
        verbose_name = _("Uploaded Text File")
        verbose_name_plural = _("Uploaded Text Files")
