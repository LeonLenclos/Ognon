"""This module provide control functions to navigate into Animation"""

import threading
from . import change_cursor_state

@change_cursor_state
def run(cursor):
    """Call next_frm if cursor.playing is true."""
    if cursor.playing:
        next_frm(cursor)

@change_cursor_state
def auto_run(cursor):
    """If `cursor.playing` is true, start a timer that call `run` repetively
    while `cursor.playing` is true."""
    if cursor.playing:
        run(cursor)
        fps = cursor.proj.config['play']['fps']
        threading.Timer(1/fps, auto_run, [cursor]).start()

@change_cursor_state
def play(cursor):
    """Toogle cursor playing attribute."""
    cursor.playing = not cursor.playing

@change_cursor_state
def auto_play(cursor):
    """Call play and then auto_run."""
    play(cursor)
    auto_run(cursor)

@change_cursor_state
def prev_frm(cursor):
    """Set cursor position to the previous frm."""
    cursor.set_pos(frm=cursor.get_pos('frm')-1)

@change_cursor_state
def next_frm(cursor):
    """Set cursor position to the next frm."""
    cursor.set_pos(frm=cursor.get_pos('frm')+1)

@change_cursor_state
def first_frm(cursor):
    """Set cursor position to the first animation frm."""
    cursor.set_pos(frm=0)

@change_cursor_state
def last_frm(cursor):
    """Set cursor position to the last animation frm."""
    cursor.set_pos(frm=cursor.anim_len()-1)

@change_cursor_state
def go_to_frm(cursor, i):
    """Set cursor position to frm i."""
    cursor.set_pos(frm=i)

@change_cursor_state
def go_to_layer(cursor, i):
    """Set cursor position to layer i."""
    cursor.set_pos(layer=i)

@change_cursor_state
def lower_layer(cursor):
    """Set the cutsor position to the lower layer."""
    cursor.set_pos(layer=cursor.get_pos('layer')+1)

@change_cursor_state
def upper_layer(cursor):
    """Set the cutsor position to the upper layer."""
    cursor.set_pos(layer=cursor.get_pos('layer')-1)