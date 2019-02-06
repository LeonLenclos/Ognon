"""This module provide control functions to export frms and anims"""

import itertools

import PIL.Image
import PIL.ImageDraw

from .. import projects
from .. import view

def _frm_to_pilimage(cursor, frm=None):
    """
    Create a PIL.Image object from the current animation frm or passed frm.
    """
    width = cursor.proj.config['view']['width']
    height = cursor.proj.config['view']['height']
    scale = cursor.proj.config['export']['scale']
    stroke = cursor.proj.config['view']['line_width']
    bg_color = cursor.proj.config['view']['background_color']
    line_color = cursor.proj.config['view']['line_color']

    img = PIL.Image.new("RGB", (width*scale, height*scale), bg_color)
    draw = PIL.ImageDraw.Draw(img)
        
    for line in view.get_lines(cursor, frm=frm):
        coords = [coord * scale for coord in line]
        draw.line(tuple(coords), line_color, width=stroke*scale)

    return img

def frm_to_png(cursor, frm=None):
    """
    Save the current frm on the disk as a png image.

    Location is given by export>png_name in the config file.
    """
    name_format = cursor.proj.config['export']['png_name']
    anim = cursor.get_pos('anim')
    frm = frm if frm is not None else cursor.get_pos('frm')
    path = projects.get_path(cursor, name_format.format(anim=anim, frm=frm))

    _frm_to_pilimage(cursor, frm=frm).save(path)


def anim_to_pngs(cursor):
    """
    Save all animation frms on the disk as a png images.

    Location is given by export>png_name in the config file.
    """
    for frm in range(cursor.anim_len()):
        frm_to_png(cursor, frm)

def anim_to_gif(cursor):
    """
    Save the animation on the disk as a animated gif.

    Location is given by export>gif_name in the config file.
    """
    name_format = cursor.proj.config['export']['gif_name']
    duration = 1000/cursor.proj.config['play']['fps']
    anim = cursor.get_pos('anim')
    path = projects.get_path(cursor, name_format.format(anim=anim))

    _frm_to_pilimage(cursor, 0).save(
        path,
        save_all=True,
        append_images=map(
            _frm_to_pilimage,
            itertools.repeat(cursor),
            range(1, cursor.anim_len())),
        duration=duration,
        loop=0
    )

def anim_to_avi(cursor):
    pass
