def touch(fun):
    """décorateur des methodes du model"""
    def wrapper(*args):
        ret = fun(*args)
        for l in args[0].listeners:
            l()
        return ret
    return wrapper
