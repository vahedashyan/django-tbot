from tbot.utils import get_bot


class CommandDataStructure:
    def __init__(self, name, command_type, arguments):
        self.name = name
        self.type = command_type
        self.arguments = arguments

    @property
    def input_command(self):
        return "input_command={}".format(self.name)


class CommandItem:
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class CommandGenerator:
    bot = get_bot()

    @classmethod
    def _get_command(cls, name):
        ex_function = cls.bot.commands.get(name)
        if not ex_function:
            ex_function = cls._get_default_command(name)
        return ex_function

    @classmethod
    def _get_default_command(cls, name):
        ex_function = cls.bot.default_commands.get(name)
        if not ex_function:
            ex_function = cls.bot.default_commands.get('unknown')
        return ex_function

    @classmethod
    def _get_defined_arguments(cls, arguments):
        defined_arguments = []
        undefined_arguments = []
        for argument in arguments:
            if "=" in argument:
                clear_argument = argument.split("=")
                defined_arguments.append((str(clear_argument[0]), str(clear_argument[1])))
            else:
                undefined_arguments.append(str(argument))

        return tuple(undefined_arguments), dict(defined_arguments)

    @classmethod
    def get_command_item(cls, command_structure: CommandDataStructure):
        command_function = cls._get_command(command_structure.name)
        args, kwargs = cls._get_defined_arguments(command_structure.arguments)
        command_item = CommandItem(command_function, args, kwargs)
        return command_item


class CommandBaseType:
    command_list = []
    command_item_list = []

    def __init__(self, message):
        self.message = message

    def _parse_content(self):
        raise NotImplemented

    def _define_arguments(self):
        raise NotImplemented

    def create_function_object(self):
        raise NotImplemented

    @classmethod
    def get_command(cls):
        raise NotImplemented

    @staticmethod
    def input_command(command_text):
        return "input_command={}".format(command_text)

    @property
    def entities(self):
        return self.message.get('entities')

    @property
    def location(self):
        return self.message.get('location')

    @property
    def text(self):
        return self.message.get('text')

    def get_command_name(self, command_content):
        command_name = self.text[
                       command_content.get('offset'):command_content.get('offset') + command_content.get('length')]
        return command_name

    def get_command_arguments(self, command_content):
        command_name = self.text[command_content.get('offset') + command_content.get('length'):].split('/')[0].split()
        return command_name

    def _init_commands_structures(self):
        return self._parse_content()

    def _create_command_structure(self, name, command_type, arguments):
        parsed_command = CommandDataStructure(name, command_type, arguments)
        return parsed_command

    def get_commands(self):
        command_list = self._init_commands_structures()
        command_item_list = []
        for command_item in command_list:
            command_item_list.append(CommandGenerator.get_command_item(command_item))
        return command_item_list


class TextCommand(CommandBaseType):
    def __init__(self, message):
        super().__init__(message)


class UnknownCommand(CommandBaseType):
    def __init__(self, message):
        super().__init__(message)


class LocationCommand(CommandBaseType):
    def __init__(self, message):
        super().__init__(message)


class EntityCommand(CommandBaseType):
    type = 'ENTITY'

    def __init__(self, message):
        super().__init__(message)

    def _parse_content(self):
        parsed_command_list = []
        for command_content in self.entities:
            command_name = self.get_command_name(command_content)
            command_arguments = self.get_command_arguments(command_content)
            command_arguments.append(self.input_command(command_name))
            if command_content.get('type') == 'bot_command':
                command_name = command_name.strip('/')
                parsed_command_list.append(self._create_command_structure(command_name, self.type, command_arguments))
        return parsed_command_list
