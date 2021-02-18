from django.conf import settings
from .exception import ConfigurationError, UnKnownError

# TODO: create configuration function to handle the errors during configuration process.

try:
    configs = settings.DJANGO_TBOT_CONFIGS
except AttributeError as e:
    raise ConfigurationError(e)
except Exception as e:
    raise UnKnownError(e)

COMMAND_ROOT_PATH = configs.get("COMMAND_ROOT_PATH")
TUTORIAL_BOT_TOKEN = configs.get("TUTORIAL_BOT_TOKEN")
BOT_WEBHOOK_URL = configs.get("WEBHOOK_URL")
BOT_APP_PATH = configs.get("APP_PATH")

# TODO raise specific error
if not all((COMMAND_ROOT_PATH, TUTORIAL_BOT_TOKEN, BOT_WEBHOOK_URL, BOT_APP_PATH)):
    raise ConfigurationError
