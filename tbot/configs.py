from django.conf import settings
from .exception import ConfigurationError

# TODO: create configuration function to handle the errors during configuration process.

if settings.DJANGO_TBOT_CONFIGS:
    configs = settings.DJANGO_TBOT_CONFIGS
else:
    raise ConfigurationError

COMMAND_ROOT_PATH = configs.get("COMMAND_ROOT_PATH")
TUTORIAL_BOT_TOKEN = configs.get("TUTORIAL_BOT_TOKEN")
BOT_WEBHOOK_URL = configs.get("WEBHOOK_URL")
BOT_APP_PATH = configs.get("APP_PATH")

# TODO raise specific error
if not all((COMMAND_ROOT_PATH, TUTORIAL_BOT_TOKEN, BOT_WEBHOOK_URL, BOT_APP_PATH)):
    raise ConfigurationError
