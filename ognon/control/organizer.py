"""This module provide control functions to create, delete and move elements
into layers and layers into animation"""

from ..model import Cell, Layer, AnimRef
from .navigator import next_frm, prev_frm

def add_element_after(cursor, element):
    i, _, _ = cursor.get_element_pos()
    cursor.get_layer().elements.insert(i+1, element)
    next_frm(cursor)

def add_element_before(cursor, element):
    i, _, _ = cursor.get_element_pos()
    cursor.get_layer().elements.insert(i, element)

def add_cell_after(cursor):
    add_element_after(cursor, Cell())

def add_cell_before(cursor):
    add_element_before(cursor, Cell())

def add_animref_after(cursor, name):
    add_element_after(cursor, AnimRef(name))

def add_animref_before(cursor, name):
    add_element_before(cursor, AnimRef(name))

        
def del_element(cursor):
    i, _, _ = cursor.get_element_pos()
    cursor.get_layer().elements.pop(i)

def move_element_forward(cursor):
    i, _, _ = cursor.get_element_pos()
    if i < len(cursor.get_layer().elements)-1:
        cursor.get_layer().elements.insert(i+1, _pop_element_at(cursor, i))
        next_frm(cursor)

def move_element_backward(cursor):
    i, _, _ = cursor.get_element_pos()
    if i>0:
        cursor.get_layer().elements.insert(i-1, _pop_element_at(cursor, i))
        prev_frm(cursor)

def copy_element(cursor):
    pass
    # self.add_element_after(cursor, cursor.get_frm().copy())

def clone_element(cursor):
    pass
    # if cursor.get_frm() is not None:
    #     self.add_element_after(cursor, cursor.get_frm())

def add_layer(cursor):
    idx = cursor.get_pos('layer')
    cursor.get_anim().layers.insert(idx, Layer())

def del_layer(cursor):
    pass

def move_layer_up(cursor):
    pass

def move_layer_down(cursor):
    pass

def _pop_element_at(cursor, i):
    return cursor.get_layer().elements.pop(i)