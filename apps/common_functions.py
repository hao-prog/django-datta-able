from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError


def validate_file(uploaded_file):
    allowed_mime_types = ["png", "jpg", "jpeg", "jfif", "pjpeg", "pjp"]
    result = True

    file_mime = uploaded_file.content_type.split("/")[1]
    if file_mime not in allowed_mime_types:
        result = False

    return result


def upload_file(uploaded_file, folder):
    fs = FileSystemStorage()
    name = uploaded_file.name
    file_path = folder + name

    if validate_file(uploaded_file):  # valid file
        fs.save(file_path, uploaded_file)
        return name
    else:
        raise ValidationError({'avatar': ["File must be an image!"]})