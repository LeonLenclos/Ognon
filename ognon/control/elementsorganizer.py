"""This module provide control functions to create, delete and move elements
into layers and layers into animation"""

from .. import model
from . import navigator
from . import change_project_state

@change_project_state
def add_element_after(cursor, element):
    """Add the passed element after the current frm."""
    i, _, _ = cursor.get_element_pos()
    cursor.get_layer().elements.insert(i+1, element)
    navigator.next_frm(cursor)

@change_project_state
def add_element_before(cursor, element):
    """Add the passed element before the current frm."""
    i, _, _ = cursor.get_element_pos()
    cursor.get_layer().elements.insert(i, element)

@change_project_state
def add_cell_after(cursor):
    """Add a Cell after the current frm."""
    add_element_after(cursor, model.Cell())


@change_project_state
def add_cell_before(cursor):
    """Add a Cell before the current frm."""
    add_element_before(cursor, model.Cell())

@change_project_state
def add_animref_after(cursor, name):
    """Add an AnimRef after the current frm."""
    add_element_after(cursor, model.AnimRef(name))

@change_project_state
def add_animref_before(cursor, name):
    """Add an AnimRef before the current frm."""
    add_element_before(cursor, model.AnimRef(name))

@change_project_state   
def del_element(cursor):
    """Delete the current element."""
    i, _, _ = cursor.get_element_pos()
    cursor.get_layer().elements.pop(i)

@change_project_state
def move_element_forward(cursor):
    """Move the current forward."""
    i, _, _ = cursor.get_element_pos()
    if i < len(cursor.get_layer().elements)-1:
        cursor.get_layer().elements.insert(i+1, _pop_element_at(cursor, i))
        navigator.next_frm(cursor)

@change_project_state
def move_element_backward(cursor):
    """Move the current backward."""
    i, _, _ = cursor.get_element_pos()
    if i>0:
        cursor.get_layer().elements.insert(i-1, _pop_element_at(cursor, i))
        navigator.prev_frm(cursor)

@change_project_state
def copy_element(cursor):
    """Store a copy of the current element in the special _clipboard anim."""
    raise NotImplementedError

@change_project_state
def cut_element(cursor):
    """Pop the current element to the special _clipboard anim."""
    raise NotImplementedError

@change_project_state
def paste_element(cursor):
    """Copy the content of the special _clipboard anim at the current frm."""
    raise NotImplementedError

@change_project_state
def duplicate_element(cursor):
    """Duplicate the current element."""
    raise NotImplementedError
    
def _pop_element_at(cursor, i):
    """Remove and return the element with the index i in the current layer."""
    return cursor.get_layer().elements.pop(i)
