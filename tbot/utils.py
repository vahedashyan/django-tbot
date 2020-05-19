from . import configs
from django.utils.module_loading import import_string


def get_bot():
    return import_string(configs.BOT_APP_PATH)
