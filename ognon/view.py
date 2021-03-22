"""
This module contain bunch of stateless functions. They all takes a
:class:`Cursor` object as first argument and return a JSON serializable value.
"""

import os

from . import model
from . import projects
from . import PROJECTS_DIR
from .cursor import UndefinedProjectError

from . import tags


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

def get_projects(cursor):
    """
    Return a list of all projects in the projects dir
    """
    return sorted([proj for proj in projects.get_saved_projects_list()])

def get_view_config(cursor, option=None):
    """
    Return the projects view configuration.

    If an option arg is passed, return the specified option.
    """
    if option:
        return cursor.proj.config['view'][option]
    else:
        return cursor.proj.config['view']


def get_config(cursor):
    """
    Return the project configuration
    """
    return cursor.proj.config

def get_anims(cursor):
    """
    Return a list of the projects' anims.
    """
    return sorted([anim for anim in cursor.proj.anims])

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
    Each element is describe as a dict with elements infos from get_element_infos.

    So the output may look like this :
    ::

        {
            'len':4,
            'layers':[
                [{...}],
                [{...}, {...}],
                [{...}, {...}]
            ]
        }
    """
    # TODO: add an 'empty' key in element dict
    return {
        'len':cursor.anim_len(),
        'layers':[[get_element_infos(cursor, element=element)
                for element in layer.elements]
            for layer in cursor.get_anim().layers]
    }

def get_cursor_infos(cursor):
    """
    Return a dict containing informations about the cursor state

    keys are : 'project_name', 'playing', 'clipboard', 'anim', 'frm', 'layer'
    """
    infos = {
        'project_name':cursor.proj.name,
        'playing':cursor.playing,
        'clipboard':cursor.clipboard is not None,
    }
    # infos.update(cursor._pos) DEL ?
    infos.update(cursor.get_pos())
    return infos

def get_project_defined(cursor):
    """
    Return True or False if the cursor has a project defined.
    """
    try:
        return cursor.proj is not None
    except UndefinedProjectError:
        return False

def get_element_infos(cursor, anim=None, layer=None, frm=None, element=None):
    """
    Return a dict containing informations about the current element
    keys are : 'type', 'len', 'tags', 'name'

    Alternatives frm index and anim name can be passed.
    If an element is passed, return element infos and ignore position args.
    """
    e = element if element is not None else cursor.get_element(anim, layer, frm)

    try:
        empty = len(e.lines)==0
    except AttributeError:
        empty = False

    infos = {
        'type':type(e).__name__,
        'len':cursor.element_len(e),
        'tags':e.tags,
        'name':e.name if hasattr(e ,'name') else None,
    }
    return infos

def get_lines(cursor, anim=None, frm=None, playing=None):
    """
    Return all current visible lines as a list of dict.

    Each dict has 'coords' and specials lines dict also has a 'line_type' key.

    Alternatives frm index, anim name and playing value can be passed.
    """
    playing = playing if playing is not None else cursor.playing

    lines = []

    if not playing :
        lines += get_onion_skin(cursor)

    for i in range(len(cursor.get_anim(anim).layers)):
        try:
            pos = _, element, at = cursor.get_element_pos(anim, i, frm)
        except TypeError:
            continue

        # get lines from cell
        if type(element) is model.Cell:
            element_lines = [{'coords': line.coords} for line in element.lines]
        # get lines from animref
        elif type(element) is model.AnimRef:
            element_lines = get_lines(cursor, element.name, at, True)
        else:
            continue

        for line in element_lines:

            # add 'selected' if not playing
            if not playing and pos == cursor.get_element_pos():
                line['line_type'] = line.get('line_type', set()).union({'selected'})

            # calculate tags
            for tag in element.tags:
                line['coords'] = tags.calculate_coords(line['coords'],
                    playing, at, cursor.element_len(element), tag)
                line_type = tags.calculate_line_type(line.get('line_type', set()), playing, tag)
                if line_type:
                    line['line_type'] = line_type

        lines += element_lines

    return lines


def get_drawing(cursor):
    # WARNING : untested
    return {
        'playing': cursor.playing,
        'lines':get_lines(cursor)
    }

def get_onion_skin(cursor, anim=None, frm=None):
    """
    Return a list of onion skin lines.
    """
    frm = frm if frm is not None else cursor.get_pos('frm')
    lines=[]
    lines += [{
            'coords':line['coords'],
            'line_type':line.get('line_type', set()).union({'onion_skin_backward'})
        }
        for line in get_lines(cursor, anim=anim, frm=cursor.constrain_frm(frm-1), playing=True)]
    lines += [{
            'coords':line['coords'],
            'line_type':line.get('line_type', set()).union({'onion_skin_forward'})
        }
        for line in get_lines(cursor, anim=anim, frm=cursor.constrain_frm(frm+1), playing=True)]

    return lines