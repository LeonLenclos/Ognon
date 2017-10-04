def operation(*args, **kwargs):
    def _operation(fun):
        return Operation(fun, *args, **kwargs)
    return _operation


class Operation():
    """docstring for Operation"""
    dic = {}

    def __init__(self, fun, *args, **kwargs):
        self.name = "NONE"
        self.shortcut = ""
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'shortcut' in kwargs:
            self.shortcut = kwargs['shortcut']

        self.args_required = args
        self._fun = fun
        self.target = None
        if fun.__module__ not in Operation.dic:
            Operation.dic[fun.__module__] = {}
        Operation.dic[fun.__module__][fun.__name__] = self

    def __get__(self, obj, objtype):
        """Support instance methods."""
        import functools
        return functools.partial(self.__call__, obj)

    def __call__(self, *args):
        #self = args[0]
        if len(args) == len(self.args_required) + 1:
            return self._fun(*args)
        else:
            return self._fun(self.target)
