from tbot.types import LocationCommand, TextCommand, EntityCommand, CommandDataStructure, UnknownCommand, CommandItem
from tbot.utils import get_bot
from tbot.factory import CommandFactory


class CommandProcessor:

    def __init__(self, message):
        self.bot = get_bot()
        self.message = message

    def _get_commands(self):
        commands_type = CommandFactory.get_command_type(self.message_type)
        return commands_type(self.message).get_commands()

    def run_commands(self):
        command_items_list = self._get_commands()
        for command in command_items_list:
            self._execute_command(command)

    def _execute_command(self, command_item: CommandItem):
        func = command_item.func
        try:
            func(chat_id=self.chat_id, *command_item.args, **command_item.kwargs)
        except Exception as e:
            message = "Required arguments does not exist."
            self.throw_invalid_command(error_command='error', message=message, *(),
                                       **command_item.kwargs)

    @property
    def chat_id(self):
        return self.message.get('chat')['id']

    @property
    def message_type(self):
        return self.message.get('type')

    # TODO handle exceptions
    def throw_invalid_command(self, error_command, message, *args, **kwargs):
        self.get_command_from_registered(error_command)(self.chat_id, message, *args, **kwargs)

    def get_command_from_registered(self, name=None):
        ex_function = self.bot.commands.get(name)
        if not ex_function:
            ex_function = self.bot.default_commands.get(name)
        return ex_function
