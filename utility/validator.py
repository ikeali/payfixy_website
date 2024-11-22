from django.core.exceptions import ValidationError
import requests

def validate_file_type(value):
    allowed_types = ['pdf', 'jpg', 'jpeg', 'png']
    ext = value.name.split('.')[-1].lower()  # Get the file extension
    if ext not in allowed_types:
        raise ValidationError(f'Unsupported file type: {ext}. Allowed types: {", ".join(allowed_types)}')


