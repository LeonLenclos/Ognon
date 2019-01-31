"""This module provide control functions to navigate into Animation"""

from threading import Timer

def run(cursor):
    if cursor.playing:
        next_frm(cursor)

def auto_run(cursor):
    if cursor.playing:
        run(cursor)
        fps = int(cursor.proj.config['play']['fps'])
        Timer(1/fps, auto_run, [cursor]).start()

def play(cursor):
    """Permet de lire ou de stopper l'anim"""
    cursor.playing = not cursor.playing
    # OLD => 
    # if cursor.playing and cursor.proj.config['play']['auto_run'] == 'true':
    #     auto_run(cursor)

def prev_frm(cursor):
    """Permet d'acceder à la frm précédente"""
    cursor.set_pos(frm=cursor.get_pos('frm')-1)

def next_frm(cursor):
    """Permet d'acceder à la frm suivante"""
    cursor.set_pos(frm=cursor.get_pos('frm')+1)

def first_frm(cursor):
    """Permet d'acceder à la frm suivante"""
    cursor.set_pos(frm=0)

def last_frm(cursor):
    """Permet d'acceder à la frm précédente"""
    cursor.set_pos(frm=cursor.anim_len()-1)

def go_to_frm(cursor, i):
    """Permet d'acceder à une frm i"""
    cursor.set_pos(frm=i)

def go_to_layer(cursor, i):
    cursor.set_pos(layer=i)
