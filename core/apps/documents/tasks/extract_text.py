from celery import shared_task
from apps.documents.utils.document_helpers import (
    extract_pdf_text,
    should_extract_text_for_type,
)
import logging
from apps.documents.models import Document, UploadedTextFile
import gc 


logger = logging.getLogger(__name__)


@shared_task(queue="tasks")
def extract_text_from_document(document_id):
    try:
        document = Document.objects.select_related("document_type").get(pk=document_id)

        # Extract text
        text = extract_pdf_text(document.file.path)

        # Clean up memory immediately after extraction
        gc.collect()

        if text:
            UploadedTextFile.objects.create(
                text=text, document=document, document_type=document.document_type
            )
            return "Text extracted and saved successfully"
        return "Empty or failed extraction"

    except Document.DoesNotExist:
        return "Document not found"

    except Exception as e:
        logger.error(f"Document text extraction failed: {e}")
        return f"Extraction failed: {str(e)}"
