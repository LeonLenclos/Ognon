"""
This package contain bunch of stateless functions. organized into modules.
They all takes a :class:`Cursor` object as first argument and does not return
any value.
"""
def change_project_state(fun):
    """
    This decorator is for control function that change the project state.
    It make the function increment the project's state_id before doing stuff.
    """
    def wrapped(cursor, *args, **kwargs):
        cursor.proj.state_id += 1
        return fun(cursor, *args, **kwargs)
    return wrapped

def change_project_draw_state(fun):
    """
    This decorator is for control function that change the project draw state.
    It make the function increment the project's draw_state_id before doing stuff.
    """
    def wrapped(cursor, *args, **kwargs):
        cursor.proj.draw_state_id += 1
        return fun(cursor, *args, **kwargs)
    return wrapped

from . import animsmanager
from . import drawer
from . import navigator
from . import elementsorganizer
from . import exporter
from . import layersorganizer
from . import projectmanager
from . import tagger
