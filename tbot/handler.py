from builtins import property

from .command import Command
from .processor import CommandProcessor
from .utils import get_bot
import inspect


class BotUpdateHandler(object):
    bot = get_bot()

    def __init__(self, update):
        self.update = update
        self._process_commands()

    def _process_commands(self):
        if not self.message:
            raise NotImplementedError
        CommandProcessor(message=self.message).run_commands()

    @property
    def message(self):
        message = self.update.get('message', self.update.get('edited_message'))
        message = self._get_message_with_type(message)
        return message

    @staticmethod
    def _get_message_with_type(message):
        if message.get('location'):
            message['type'] = 'location'
            return message
        if message.get('entities'):
            message['type'] = 'entity'
            return message
        if message.get('text'):
            message['type'] = 'text'
            return message
        else:
            message['type'] = 'unknown'
            return message
