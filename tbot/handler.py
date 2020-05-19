from .utils import get_bot


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
        if self.entities:
            command_list, _ = self.parse_text()
            for command_name in command_list:
                ex_functions.append({'function': self.get_command_from_registered(command_name),
                                     'args': (),
                                     'kwargs': {'input_command': command_name}})
        elif self.text:
            ex_functions.append({'function': self.get_command_from_registered('unknown'),
                                 'args': (),
                                 'kwargs': {'input_command': self.text}})
        return ex_functions

    def parse_text(self):
        command_list = []
        text_command_list = []
        for command in self.entities:
            command_text = self.text[command.get('offset'):command.get('offset') + command.get('length')]
            if "/" in command_text:
                command_list.append(command_text.strip('/'))
            else:
                text_command_list.append(command_text)
        return command_list, text_command_list

    def run_commands(self):
        function_list = self.get_commands()
        for function_item in function_list:
            f = function_item.get('function')
            args = function_item.get('args')
            kwargs = function_item.get('kwargs')

            if callable(f) and isinstance(f, object):
                f(self.chat_id, (), *args, **kwargs)
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