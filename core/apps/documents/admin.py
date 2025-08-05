from django.contrib import admin
from .models import DocumentCategory, DocumentType, Document, UploadedTextFile


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "company_id", "participant", "is_deleted")
    list_filter = ("is_deleted",)
    search_fields = ("title",)


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "private_visible", "public_visible", "is_active", "is_deleted")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("title",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("company_id", "participant", "document_type", "is_active", "is_deleted")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("document_type__title",)


@admin.register(UploadedTextFile)
class UploadedTextFileAdmin(admin.ModelAdmin):
    list_display = ("document_type", "document", "short_text")

    def short_text(self, obj):
        return obj.text[:50]
    short_text.short_description = "Text Preview"
