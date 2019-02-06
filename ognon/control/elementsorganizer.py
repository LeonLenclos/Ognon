"""This module provide control functions to create, delete and move elements
into layers and layers into animation"""

from .. import model
from . import navigator

def add_element_after(cursor, element):
    """Add the passed element after the current frm."""
    i, _, _ = cursor.get_element_pos()
    cursor.get_layer().elements.insert(i+1, element)
    navigator.next_frm(cursor)

def add_element_before(cursor, element):
    """Add the passed element before the current frm."""
    i, _, _ = cursor.get_element_pos()
    cursor.get_layer().elements.insert(i, element)

def add_cell_after(cursor):
    """Add a Cell after the current frm."""
    add_element_after(cursor, model.Cell())

def add_cell_before(cursor):
    """Add a Cell before the current frm."""
    add_element_before(cursor, model.Cell())

def add_animref_after(cursor, name):
    """Add an AnimRef after the current frm."""
    add_element_after(cursor, model.AnimRef(name))

def add_animref_before(cursor, name):
    """Add an AnimRef before the current frm."""
    add_element_before(cursor, model.AnimRef(name))

        
def del_element(cursor):
    """Delete the current element."""
    i, _, _ = cursor.get_element_pos()
    cursor.get_layer().elements.pop(i)

def move_element_forward(cursor):
    """Move the current forward."""
    i, _, _ = cursor.get_element_pos()
    if i < len(cursor.get_layer().elements)-1:
        cursor.get_layer().elements.insert(i+1, _pop_element_at(cursor, i))
        navigator.next_frm(cursor)

def move_element_backward(cursor):
    """Move the current backward."""
    i, _, _ = cursor.get_element_pos()
    if i>0:
        cursor.get_layer().elements.insert(i-1, _pop_element_at(cursor, i))
        navigator.prev_frm(cursor)

def copy_element(cursor):
    pass
    # self.add_element_after(cursor, cursor.get_frm().copy())

def clone_element(cursor):
    pass
    # if cursor.get_frm() is not None:
    #     self.add_element_after(cursor, cursor.get_frm())

def _pop_element_at(cursor, i):
    """Remove and return the element with the index i in the current layer."""
    return cursor.get_layer().elements.pop(i)
