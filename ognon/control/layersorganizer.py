"""
This module provide control functions to create, delete layers into animation.
"""

from .. import model
from . import navigator
from . import change_project_state
from . import change_cursor_state

@change_project_state
def add_layer(cursor):
    """Add a new Layer to the anim."""
    idx = cursor.get_pos('layer')
    cursor.get_anim().layers.insert(idx, model.Layer())

@change_project_state
@change_cursor_state
def del_layer(cursor):
    """Delete the the current layer from the anim."""
    _pop_layer_at(cursor, cursor.get_pos('layer'))

@change_project_state
def move_layer_up(cursor):
    """Move up the current layer."""
    i = cursor.get_pos('layer')
    cursor.get_anim().layers.insert(i-1, _pop_layer_at(cursor, i))

@change_project_state
def move_layer_down(cursor):
    """Move down the current layer."""
    i = cursor.get_pos('layer')
    cursor.get_anim().layers.insert(i+1, _pop_layer_at(cursor, i))

def _pop_layer_at(cursor, i):
    """Remove and return the layer with the index i in the current anim."""
    return cursor.get_anim().layers.pop(i)
