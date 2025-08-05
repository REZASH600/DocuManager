import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_pdf_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext != '.pdf':
        raise ValidationError(_("Only PDF files are allowed."))