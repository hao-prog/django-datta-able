import os
from django.core.files.storage import FileSystemStorage


def validate_file(uploaded_file):
    allowed_mime_types = ["png", "jpg", "jpeg", "jfif", "pjpeg", "pjp"]
    message = None

    file_mime = uploaded_file.content_type.split("/")[1]
    if len(allowed_mime_types) > 0:
        if file_mime not in allowed_mime_types:
            message = ["File must be an image!"]

    return message


def upload_file(uploaded_file, folder, file_path_tmp, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(os.path.dirname(folder_path))

    fs = FileSystemStorage()

    file_path = folder + uploaded_file.name
    if fs.exists(file_path_tmp):
        fs.delete(file_path_tmp)
    if fs.exists(file_path):
        fs.delete(file_path)

    fs.save(file_path, uploaded_file)


def move_tmp_file(folder_path, file_path_tmp, avatar_tmp):
    file_path_tmp_os = "apps/static/assets/images/" + file_path_tmp
    file_path_os = folder_path + avatar_tmp
    os.rename(file_path_tmp_os, file_path_os)