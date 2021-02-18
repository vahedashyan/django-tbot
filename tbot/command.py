import inspect


class Command(object):
    _func = None
    _arguments = ()
    _argument_serializer = None
    _name = "default_func"

    def __init__(self, name, args=None, argument_serializer=None):
        self._name = name
        if args:
            self._arguments = args
        if argument_serializer:
            self._argument_serializer = argument_serializer

    @property
    def run(self):
        return self.func()

    def get_args(self):
        return inspect.getargs(self.func)
