from builtins import property

from .command import Command
from .utils import get_bot
import inspect


class BotUpdateHandler(object):
    bot = get_bot()

    def __init__(self, update):
        self.update = update
        self.run_commands()

    def get_commands(self):
        ex_functions = []
        if not self.message:
            raise NotImplementedError
        if self.location:
            ex_function = self.get_command_from_registered('location')
            ex_functions.append({'function': self.get_command_from_registered('location'),
                                 'args': (),
                                 'kwargs': self.location})
            ex_functions.append(self.make_command_function_dict(name='location', arguments=self.location))

        if self.entities:
            command_list = self.parse_text()
            for command in command_list:
                command_name = command.get('name')
                command_arguments = command.get('arguments')
                ex_functions.append(self.make_command_function_dict(name=command_name, arguments=command_arguments))
        elif self.text:
            ex_functions.append(
                self.make_command_function_dict(name='unknown', arguments=[self.input_command(self.text)]))
        return ex_functions

    def make_command_function_dict(self, name, arguments=None):
        command = self.get_command_from_registered(name)
        undefined_arguements = ()
        defined_arguments = {}
        if arguments:
            defined_arguments, undefined_arguements = self._define_arguments(arguments)

        command_dict = {'command': command,
                        'args': tuple(undefined_arguements),
                        'kwargs': dict(defined_arguments)}
        return command_dict

    def _define_arguments(self, argument_list):
        defined_arguments = []
        undefined_arguemtns = []
        for argument in argument_list:
            if "=" in argument:
                clear_argument = argument.split("=")
                defined_arguments.append((str(clear_argument[0]), str(clear_argument[1])))
            else:
                undefined_arguemtns.append(str(argument))

        return defined_arguments, undefined_arguemtns

    def parse_text(self):
        command_list = []
        for command in self.entities:
            command_dict = {}
            command_text = self.text[command.get('offset'):command.get('offset') + command.get('length')]
            command_arguments = self.text[command.get('offset') + command.get('length'):].split('/')[0].split()
            command_arguments.append(self.input_command(command_text))

            if command.get('type') == 'bot_command':
                command_dict['name'] = command_text.strip('/')
                command_dict['arguments'] = command_arguments
                command_list.append(command_dict)
        return command_list

    def run_commands(self):
        commands_list = self.get_commands()
        for command_item in commands_list:
            command = command_item.get('command')
            args = command_item.get('args')
            kwargs = command_item.get('kwargs')

            if isinstance(command, Command):
                try:
                    command(self.chat_id, *args, **kwargs)
                except TypeError as e:
                    message = "Required arguments does not exist."
                    self.get_command_from_registered('error')(self.chat_id, message, *args, **kwargs)

            else:
                self.throw_invalid_command(*args, **kwargs)

    def throw_invalid_command(self, *args, **kwargs):
        self.get_command_from_registered('unknown')(self.chat_id, *args, **kwargs)

    def get_command_from_registered(self, name=None):
        ex_function = self.bot.commands.get(name)
        if not ex_function:
            ex_function = self.bot.default_commands.get(name)
        return ex_function

    @staticmethod
    def input_command(command_text):
        return "input_command={}".format(command_text)

    @property
    def message(self):
        return self.update.get('message')

    @property
    def chat_id(self):
        return self.message.get('chat')['id']

    @property
    def entities(self):
        return self.message.get('entities')

    @property
    def location(self):
        return self.message.get('location')

    @property
    def text(self):
        return self.message.get('text')
