"""This module provide control functions to manage project's anims"""

from .. import model
from . import change_project_state
from . import change_cursor_state

@change_cursor_state
def new_anim(cursor, name):
    """Add a new Anim to anims dict."""
    cursor.proj.anims[name] = model.Anim()

@change_cursor_state
def select_anim(cursor, name):
    """Set cursor anim name. If anim does not exists, create it."""
    if name not in cursor.proj.anims:
	    new_anim(cursor, name)
    cursor.set_pos(anim=name)

@change_project_state
def del_anim(cursor, name):
    """Delete an Anim from anims dict."""
    del cursor.proj.anims[name]

@change_project_state
def new_animref(cursor, name):
    """
    Create a new anim, add current element to it
    and replace current element by an Animref linking to it.
    """
    i, e, _ = cursor.get_element_pos()
    new_anim(cursor, name)
    cursor.get_layer(anim=name, layer=0).elements = [e]
    cursor.get_layer().elements[i]=model.AnimRef(name)

@change_cursor_state
def select_animref(cursor):
    """Set cursor anim name from current animref."""
    _, e, _ = cursor.get_element_pos()
    select_anim(cursor, e.name)