from .model import Cell, AnimRef

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

def get_lines(cursor, frm=None):
    lines=[]
    for i in range(len(cursor.get_anim().layers)):
        pos = cursor.get_element_pos(layer=i, frm=frm)
        if pos is not None:
            _, element, at = pos
            if type(element) is Cell:
                lines += [line.coords for line in element.lines]
            if type(element) is AnimRef:
                index, element, at = cursor.get_element_pos(layer=i)
                lines += get_lines(cursor, anim=element.name, frm=at)

    return lines

def get_onion_skin(cursor):
    frm = cursor.get_pos('frm')
    return {
        -1: get_lines(cursor, frm=cursor.constrain_frm(frm-1)),
        1: get_lines(cursor, frm=cursor.constrain_frm(frm+1)),
    }