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
            ex_functions.append(self.make_command_function_dict(name='unknown'))
        return ex_functions

    def make_command_function_dict(self, name, arguments=None):
        funtion = self.get_command_from_registered(name)
        undefined_arguements = ()
        defined_arguments = {}
        if arguments:
            defined_arguments, undefined_arguements = self._define_arguments(arguments)

        funct_dict = {'function': funtion,
                      'args': tuple(undefined_arguements),
                      'kwargs': dict(defined_arguments)}
        return funct_dict

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
        arguments = []
        for command in self.entities:
            command_dict = {}
            command_text = self.text[command.get('offset'):command.get('offset') + command.get('length')]
            command_arguemts = self.text[command.get('offset') + command.get('length'):].split('/')[0].split()
            print({"command": command_text, "arguments": command_arguemts})

            if command.get('type') == 'bot_command':
                command_dict['name'] = command_text.strip('/')
                command_dict['arguments'] = command_arguemts
                command_list.append(command_dict)
        return command_list

    def run_commands(self):
        function_list = self.get_commands()
        for function_item in function_list:
            f = function_item.get('function')
            args = ("afwdgsebsebrtbserb",)
            kwargs = function_item.get('kwargs')

            if callable(f) and isinstance(f, object):
                defined_args = set(inspect.getargs(f.__code__).args).intersection(set(kwargs.keys()))
                try:
                    f(self.chat_id, **kwargs)
                except TypeError as e:
                    message = "Required arguments does not exist."
                    self.get_command_from_registered('error')(self.chat_id, message, *args, **kwargs)

            else:
                self.throw_invalid_command(*args, **kwargs)

    def throw_invalid_command(self, *args, **kwargs):
        self.get_command_from_registered('unknown')(chat_id=self.chat_id, *args, **kwargs)

    def get_command_from_registered(self, name=None):
        ex_function = self.bot.commands.get(name)
        if not ex_function:
            ex_function = self.bot.default_commands.get(name)
        return ex_function

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