import inspect

import importlib
from tbot import configs
from telegram import Bot, ChatAction


class BotApp(Bot):
    commands = {}
    default_commands = {}
    commands_path = configs.COMMAND_ROOT_PATH
    default_commands_path = 'tbot.commands'
    bot_name = "ABC"

    def __init__(self, bot_name=None):
        if bot_name:
            self.bot_name = bot_name
        super(BotApp, self).__init__(token=configs.TUTORIAL_BOT_TOKEN)

    def make_configs(self):
        print('{} configured'.format(self.name))

    def command(self, command_name=None, default=True):
        def decorator(f):  # TODO  handle the case with duplicate command names
            if inspect.getmodule(f).__name__ == self.default_commands_path:
                self.default_commands.update({command_name: f})
            else:
                self.commands.update({command_name: f})
            return f

        return decorator

    def _register_commands(self):
        importlib.import_module(self.commands_path)
        importlib.import_module(self.default_commands_path)
        print(self.commands.keys())
        print(self.default_commands.keys())

    def start(self):
        self._register_commands()

    def action_typing(self, chat_id):
        self.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)


def create_bot():
    bot = BotApp()
    bot.make_configs()
    return bot
