from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.middleware.csrf import rotate_token
from django.shortcuts import redirect

SESSION_KEY = "_auth_account_id"
TYPE_SESSION_KEY = "_is_admin"


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
        raise ValidationError({"avatar": ["File must be an image!"]})


def login(request, user):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    """

    if user is None:
        user = request.user

    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != str(user.pk):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()

    request.session[SESSION_KEY] = str(user.pk)
    request.session[TYPE_SESSION_KEY] = user.is_admin
    if hasattr(request, "user"):
        request.user = user

    rotate_token(request)


def login_required():
    def inner(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            if not SESSION_KEY in request.session:
                return redirect("/login/")
            return func(*args, **kwargs)

        return wrapper

    return inner


def logout(request):
    request.session.flush()
    return redirect("/login/")
