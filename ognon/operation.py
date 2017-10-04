class Operation():
    """docstring for Operation"""
    dic = {}

    def __init__(self, fun):
        self._fun = fun
        if fun.__module__ not in Operation.dic:
            Operation.dic[fun.__module__] = {}
        Operation.dic[fun.__module__][fun.__name__] = self

    def __get__(self, obj, objtype):
        """Support instance methods."""
        import functools
        return functools.partial(self.__call__, obj)

    def __call__(self, *args, **kwargs):
        return self._fun(*args, **kwargs)
