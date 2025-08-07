from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.documents"
    verbose_name = "Document"
    verbose_name_plural = "Documents"

    def ready(self):
        from apps.documents.signals import (
            document_category_signals,
            document_signals,
            document_type_signals,
        )
