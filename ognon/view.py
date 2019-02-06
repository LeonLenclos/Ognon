"""
This module contain bunch of stateless functions. They all takes a
:class:`Cursor` object as first argument and return a JSON serializable value.
"""

import os

from . import model
from . import projects
from . import PROJECTS_DIR

def get_path(cursor, file=""):
    """
    Return path to the project (or path to a file in the project).
    """
    return os.path.join(PROJECTS_DIR, cursor.proj.name, file)

def get_projects_tree(cursor):
    """
    Return a dict withs all projects in the projects dir as keys and a list of
    the projects' anims as values
    """
    list_anims = lambda p: [
        file[:-4]
        for file in os.path.join(PROJECTS_DIR, p)
        if file.endswith('.ogn')
    ]
    
    return {
        project_name:list_anims(project_name)
        for project_name in projects.get_saved_projects_list()
    }

def get_view_config(cursor, option=None):
    """
    Return the projects view configuration.

    If an option arg is passed, return the specified option.
    """
    if option:
        return cursor.proj.config['view'][option]
    else:
        return cursor.proj.config['view']

def get_anims(cursor):
    """
    Return a list of the projects' anims.
    """
    return [anim for anim in cursor.proj.anims]

def get_playing(cursor):
    """
    Return the value of cursor.playing
    """
    return cursor.playing

def get_timeline(cursor):
    """
    Return a dict with informations about organization of the anim.

    The 'len' field contain the animation length. 
    The 'layers' field contain a list of layers as lists of elements. 
    Each element is describe as a dict with his type and his length.

    So the output may look like this :
    ::

        {
            'len':4,
            'layers':[
                [{'len':1, 'type':'Cell'}],
                [{'len':1, 'type':'Cell'}, {'len':1, 'type':'Cell'}],
                [{'len':1, 'type':'Cell'}, {'len':3, 'type':'Animref'}]
            ]
        }
    """
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
    """
    Return a dict containing informations about the cursor state

    keys are : 'project_name', 'playing', 'loop', 'anim', 'frm', 'layer'
    """
    infos = {
        'project_name':cursor.proj.name,
        'playing':cursor.playing,
        'loop':cursor.loop,
    }
    infos.update(cursor.get_pos())
    return infos

def get_lines(cursor, frm=None, anim=None):
    """
    Return a list of all current lines.

    Alternatives frm index and anim name can be passed.

    The output is a list of lists since ognon lines can be describe as list of
    coords. (e.g. [x1, y1, x2, y2, x3, y3])
    """
    lines=[]
    for i in range(len(cursor.get_anim(anim).layers)):
        pos = cursor.get_element_pos(layer=i, frm=frm, anim=anim)
        if pos is not None:
            _, element, at = pos
            if type(element) is model.Cell:
                lines += [line.coords for line in element.lines]
            if type(element) is model.AnimRef:
                index, element, at = cursor.get_element_pos(layer=i, anim=anim)
                lines += get_lines(cursor, anim=element.name, frm=at)

    return lines

def get_onion_skin(cursor, onion_range=(0,)):
    """
    Return a dict of anim lines.

    Keys are given by the onion_range arg and are the frm to look at, relatively
    to the current frm. (eg. `onion_range=(-1,0)` means : 'look at the current
    frm and the previous frm')

    Values are given by the get_lines function passing the frm argument.
    """
    frm = cursor.get_pos('frm')
    return {
        idx: get_lines(cursor, frm=cursor.constrain_frm(frm+idx))
        for idx in onion_range
    }
