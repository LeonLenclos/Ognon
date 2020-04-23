"""This module provide control functions to export frms and anims"""

# NOTE : consider mooving from PIL to aggdraw or cairo

import itertools

import PIL.Image
import PIL.ImageDraw

from .. import projects
from .. import view

class ExportDestNotFoundError(FileNotFoundError):
    """This error is raised when the destination directory for exporting is
    not found."""
    pass
        
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

    # super sampling is for antialiasing resize
    supersampling = 4
    scale *= supersampling

    img = PIL.Image.new("RGB", (width*scale, height*scale), bg_color)
    draw = PIL.ImageDraw.Draw(img)
        
    for line in view.get_lines(cursor, frm=frm):
        coords = [coord * scale for coord in line]
        coords_grouped = [(x, y) for x, y in zip(*[iter(coords)]*2)]
        draw.line(tuple(coords_grouped), fill=line_color, width=stroke*scale, joint='curve')

    img = img.resize((int(width*scale/supersampling), int(height*scale/supersampling)), PIL.Image.ANTIALIAS)
    return img

def _frm_to_img(cursor, ext, frm=None):
    """
    Save the current frm or the given frm on the disk as an image.

    ext must be an image file extension supported by pillow
    and for which a path is given in the config file.
    """
    name_format = cursor.proj.config['export'][ext+'_name']
    anim = cursor.get_pos('anim')
    frm = frm if frm is not None else cursor.get_pos('frm')
    path = view.get_path(cursor, name_format.format(anim=anim, frm=frm))

    try:
        _frm_to_pilimage(cursor, frm=frm).save(path)
    except FileNotFoundError:
        raise ExportDestNotFoundError()    

def _anim_to_imgs(cursor, ext):
    """
    Save all animation frms on the disk as a images.

    ext must be an image file extension supported by pillow
    and for which a path is given in the config file.
    """
    for frm in range(cursor.anim_len()):
        _frm_to_img(cursor, ext, frm)

def frm_to_png(cursor, frm=None):
    """
    Save the current frm on the disk as a png image.
    """
    _frm_to_img(cursor, 'png', frm)  

def frm_to_tga(cursor, frm=None):
    """
    Save the current frm on the disk as a png image.
    """
    _frm_to_img(cursor, 'tga', frm)  


def anim_to_pngs(cursor):
    """
    Save all animation frms on the disk as a png images.
    """
    _anim_to_imgs(cursor, 'png')  

def anim_to_tgas(cursor):
    """
    Save all animation frms on the disk as a tgas images.
    """
    _anim_to_imgs(cursor, 'tga')  

def anim_to_gif(cursor):
    """
    Save the animation on the disk as a animated gif.

    Location is given by export>gif_name in the config file.
    """
    name_format = cursor.proj.config['export']['gif_name']
    duration = 1000/cursor.proj.config['play']['fps']
    anim = cursor.get_pos('anim')
    path = view.get_path(cursor, name_format.format(anim=anim))

    options = {
        'save_all':True,
        'append_images':map(
            _frm_to_pilimage,
            itertools.repeat(cursor),
            range(1, cursor.anim_len())),
        'duration':duration,
    }

    if cursor.proj.config['play']['loop']:
        options['loop'] = 0

    try:
        _frm_to_pilimage(cursor, 0).save(path, **options)
    except FileNotFoundError:
        raise ExportDestNotFoundError()

def anim_to_avi(cursor):
    """
    Save the animation on the disk as an avi video.

    Location is given by export>avi_name in the config file.
    """
    raise NotImplementedError
