import pdftotext

def extract_pdf_text(file_path):
    """
    Extract text content from a PDF file using pdftotext.
    High accuracy and better layout preservation.
    """
    try:
        with open(file_path, "rb") as f:
            pdf = pdftotext.PDF(f)
        return "\n\n".join(pdf)
    except Exception as e:
        print(f"[PDF ERROR]: {e}")
        return None


def should_extract_text_for_type(document_type):
    """
    Check if conditions are met for extracting text:
    - DocumentType is active
    - Not deleted
    - At least one of private_visible or public_visible is True
    """
    return (
        document_type.is_active and
        not document_type.is_deleted and
        (document_type.private_visible or document_type.public_visible)
    )



def should_extract_text_for_document(document):
    """
    Check if the given document meets the conditions for text extraction:
    - Document is active
    - DocumentType is eligible (active, not deleted, and visible)
    """
    doc_type = document.document_type
    return (
        document.is_active and
        not document.is_deleted and
        should_extract_text_for_type(doc_type)
    )