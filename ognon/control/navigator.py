"""This module provide control functions to navigate into Animation"""

import threading

def run(cursor):
    """Call next_frm if cursor.playing is true."""
    if cursor.playing:
        next_frm(cursor)

def auto_run(cursor):
    """If `cursor.playing` is true, start a timer that call `run` repetively
    while `cursor.playing` is true."""
    if cursor.playing:
        run(cursor)
        fps = cursor.proj.config['play']['fps']
        threading.Timer(1/fps, auto_run, [cursor]).start()

def play(cursor):
    """Toogle cursor playing attribute."""
    cursor.playing = not cursor.playing

def auto_play(cursor):
    """Call play and then auto_run."""
    play(cursor)
    auto_run(cursor)

def prev_frm(cursor):
    """Set cursor position to the previous frm."""
    cursor.set_pos(frm=cursor.get_pos('frm')-1)

def next_frm(cursor):
    """Set cursor position to the next frm."""
    cursor.set_pos(frm=cursor.get_pos('frm')+1)

def first_frm(cursor):
    """Set cursor position to the first animation frm."""
    cursor.set_pos(frm=0)

def last_frm(cursor):
    """Set cursor position to the last animation frm."""
    cursor.set_pos(frm=cursor.anim_len()-1)

def go_to_frm(cursor, i):
    """Set cursor position to frm i."""
    cursor.set_pos(frm=i)

def go_to_layer(cursor, i):
    """Set cursor position to layer i."""
    cursor.set_pos(layer=i)

def lower_layer(cursor):
    """Set the cutsor position to the lower layer."""
    cursor.set_pos(layer=cursor.get_pos('layer')+1)

def upper_layer(cursor):
    """Set the cutsor position to the upper layer."""
    cursor.set_pos(layer=cursor.get_pos('layer')-1)