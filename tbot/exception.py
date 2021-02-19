class TelegramBotBaseError(Exception):
    code = 1

    error_message = "UnknownError"
    success = False
    app_name = 'Tbot'

    def __init__(self, error_message=None):
        if error_message:
            self.error_message = error_message
        super(TelegramBotBaseError, self).__init__(self.message)

    @property
    def message(self):
        return "{}: {}".format(self.app_name, self.error_message)

    def serialize(self):
        return {
            "error_code": self.code,
            "error_message": self.message,
        }


    def __str__(self):
        return self.message


class UnKnownError(TelegramBotBaseError):
    code = 10
    error_message = "Unknown error."


class ConfigurationError(TelegramBotBaseError):
    code = 11
    error_message = "Configuration error."
