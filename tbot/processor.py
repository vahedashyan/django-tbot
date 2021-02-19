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
            print(e)
            print("Something goes wrong")

    @property
    def chat_id(self):
        return self.message.get('chat')['id']

    @property
    def message_type(self):
        return self.message.get('type')
