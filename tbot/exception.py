class TelegramBotExceptionBase(Exception):
    code = 1
    message = ""
    success = False

    def __init__(self, message=None):
        if message:
            self.message = message

    def serialize(self):
        return {
            "error_code": self.code,
            "error_message": self.message,
        }


class ConfigurationError(TelegramBotExceptionBase):
    code = 10
    message = "Configuration error."
