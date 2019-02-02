"""This module provide control functions to export frms and anims"""

from itertools import repeat

import PIL.Image
import PIL.ImageDraw

from .. import view


def _frm_to_pilimage(cursor, frm=None):
    width, height = 800, 600
    scale = 1
    stroke = 2
    bg_color = '#222222'
    line_color = '#FFFFFF'

    img = PIL.Image.new("RGB", (width*scale, height*scale), bg_color)
    draw = PIL.ImageDraw.Draw(img)
        
    for line in view.get_lines(cursor, frm=frm):
        coords = [coord * scale for coord in line_color]
        draw.line(coords, line_color, width=stroke*scale)

    return img

def frm_to_png(cursor, frm=None):

    anim = cursor.get_pos('anim')
    frm = frm if frm is not None else cursor.get_pos('frm')
    path = view.get_path(cursor,
        'export/{anim}-frm{frm:04d}.png'.format(anim=anim, frm=frm))

    _frm_to_pilimage(cursor, frm=frm).save(path)


def anim_to_pngs(cursor):
    for frm in range(cursor.anim_len()):
        frm_to_png(cursor, frm)

def anim_to_gif(cursor):

    anim = cursor.get_pos('anim')
    path = view.get_path(cursor,
        'export/{anim}.gif'.format(anim=anim))

    _frm_to_pilimage(cursor, 0).save(
        path,
        save_all=True,
        append_images=map(
            _frm_to_pilimage,
            repeat(cursor),
            range(1, cursor.anim_len())),
        duration=100,
        loop=0
    )

def anim_to_avi(cursor):
    pass