"""This module provide control functions to manage project's anims"""

from .. import model

def new_anim(cursor, name):
    """Add a new Anim to anims dict."""
    cursor.proj.anims[name] = model.Anim()
    select_anim(cursor, name)

def select_anim(cursor, name):
    """Set cursor anim name."""
    cursor.set_pos(anim=name)

def del_anim(cursor, name):
    """Delete an Anim from anims dict."""
    del cursor.proj.anims[name]
