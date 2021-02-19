from tbot.types import LocationCommand, TextCommand, EntityCommand, UnknownCommand


class CommandFactory:
    command_types = {
        'location': LocationCommand,
        'text': TextCommand,
        'entity': EntityCommand,
        'unknown': UnknownCommand
    }

    @classmethod
    def get_command_type(cls, message_type):
        commands_type = cls.command_types.get(message_type)
        return commands_type
