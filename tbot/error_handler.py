from functools import wraps

from django.http import JsonResponse

from .exception import TelegramBotExceptionBase


def handle_api_errors(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (TelegramBotExceptionBase,) as e:
            return JsonResponse(error_response(errors=e.serialize(), message=e.message), status=200)

    return wrapped


def successful_response(data=dict, message=""):
    return JsonResponse({
        "success": True,
        "message": message or "successful response",
        "data": data,
        "errors": {}
    })


def error_response(errors=dict, message=""):
    return {
        "success": False,
        "message": message or "error",
        "data": {},
        "errors": errors
    }
