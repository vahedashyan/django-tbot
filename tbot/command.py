import inspect


class Command(object):
    _func = None
    _arguments = ()
    _argument_serializer = None
    _name = "default_func"

    def __init__(self, name, func, args=None, kwargs=None, argument_serializer=None):
        self._name = name
        self._func = func
        if args:
            self._arguments = args
        if argument_serializer:
            self._argument_serializer = argument_serializer

    def __call__(self, chat_id, *args, **kwargs):
        # TODO vaidate args and kwargs
        return self._execute(chat_id, *args, **kwargs)

    def _execute(self, chat_id, *args, **kwargs):
        return self._func(chat_id, *args, **kwargs)

    def get_args(self):
        return inspect.getargs(self._func)

    def _define_aditional_args(self, kwargs):
        defined_args = set(inspect.getargs(self._func.__code__).args).intersection(set(kwargs.keys()))
