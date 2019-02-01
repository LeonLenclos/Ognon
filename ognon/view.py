import os

from . import model
from . import WORKING_DIR

def get_path(cursor, file=""):
    """Return path to the project (or path to a file in the project)."""
    return os.path.join(WORKING_DIR, cursor.proj.name, file)

def get_projects(cursor):
    pass

def get_anims(cursor):
    pass

def get_playing(cursor):
    return cursor.playing

def get_timeline(cursor):
    return {
        'len':cursor.anim_len(),
        'layers':[[{
            'type':type(element).__name__,
            'len':cursor.element_len(element),
            } for element in layer.elements
            ] for layer in cursor.get_anim().layers
        ],
    }

def get_cursor_infos(cursor):
    infos = {
        'project_name':cursor.proj.name,
        'playing':cursor.playing,
        'loop':cursor.loop,
    }
    infos.update(cursor.get_pos())
    return infos

def get_lines(cursor, frm=None, anim=None):
    lines=[]
    for i in range(len(cursor.get_anim(anim).layers)):
        pos = cursor.get_element_pos(layer=i, frm=frm)
        if pos is not None:
            _, element, at = pos
            if type(element) is model.Cell:
                lines += [line.coords for line in element.lines]
            if type(element) is model.AnimRef:
                index, element, at = cursor.get_element_pos(layer=i)
                lines += get_lines(cursor, anim=element.name, frm=at)

    return lines

def get_onion_skin(cursor, onion_range=(0)):
    frm = cursor.get_pos('frm')
    return {
        idx: get_lines(cursor, frm=cursor.constrain_frm(frm+idx))
        for idx in onion_range
    }
    # return {
    #     -1: get_lines(cursor, frm=cursor.constrain_frm(frm-1)),
    #     1: get_lines(cursor, frm=cursor.constrain_frm(frm+1)),
    # }