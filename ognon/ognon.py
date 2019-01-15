# /usr/bin/python3
# !
# -*-coding:Utf-8 -*

"""
Ognon is a a software application for the creation of 2D animation
Ognon est un logiciel pour la création d'animation 2D

"""

import argparse

import tkinter as tk

from interface import board, win, table
from control import recorder

ap = argparse.ArgumentParser()
ap.add_argument('-n', nargs=1, help="How many animation boards", default="1")
ap.add_argument('-i', nargs=1, help="How many images per seconds", default="6")
ap.add_argument('-w', nargs=1, help="Wich stroke weight", default="3")
ap.add_argument('-s', nargs=1, help="stroke color", default="white")
ap.add_argument('-b', nargs=1, help="bg color", default="black")
ap.add_argument('-l', action='store_true', help="Open a live board")
ap.add_argument('-o', action='store_true', help="OSC sync")

args = ap.parse_args()

env = int(args.n[0])
live = args.l
osc_sync = args.o

class Ognon(tk.Tk):
    """This class is for the application.

    It subclasses tkinter.Tk, the tkinter's main application window class.
    Show a little window with the ognon's logo"""
    def __init__(self):

        super().__init__()

        #Pref
        self.bg_color = args.b
        self.stroke_color = args.s
        self.stroke_weight = int(args.w[0])
        self.ips = int(args.i[0])

        # Size and title
        self.geometry("{}x{}".format(150, 150))
        self.title("Ognon")

        # innit of the recorder
        self.rec = recorder.Recorder("/home/leon/Projects/ANIMATIONS/OGNON/")
        self.rec.bg_color = self.bg_color
        self.rec.stroke_color = self.stroke_color
        self.rec.stroke_weight = self.stroke_weight

        # displaying ognon's logo
        self.logo = tk.BitmapImage(file="resources/logo.xbm")
        self.logo_label = tk.Label(self, image=self.logo)
        self.logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def n_anims_env(self, n, live=False):
        """ create a environment with n AnimationWindow

        If live is True, also create a BoardWindow linked to all the
        AnimationWindow (for live sessions)"""

        self.anims = []
        self.anim_wins = []

        # Create the live window
        if live:
            self.live_win = win.BoardWindow()
            self.live_win.board.bg_color = self.bg_color
            self.live_win.board.stroke_color = self.stroke_color
            self.live_win.board.stroke_weight = self.stroke_weight

        # create the clock
        self.clock_win = win.ClockWindow()
        self.clock_win.clock.ips = self.ips
        if osc_sync:
            self.clock_win.clock.osc_sync()

        # create n AnimationWindow
        for i in range(0, n):
            self.anims.append(self.rec.new_animation(width=1280, height=800))
            a = self.anims[i]
            w = win.AnimationWindow()
            w.load(a)
            w.board.bg_color = self.bg_color
            w.board.stroke_color = self.stroke_color
            w.board.stroke_weight = self.stroke_weight

            self.anim_wins.append(w)
            self.clock_win.add_navigator(w.navigator)
            if live:
                self.live_win.add_navigator(w.navigator)

    def open_ogn(self, title):
        """ Open a .ogn file

        You must first create an environment with n_anims_env. the new Animation
        will replace the first animation in self.anims"""
        a = self.rec.open_animation(title)
        self.anims[0] = a
        self.anim_wins[0].load(a)
        self.clock_win.add_navigator(self.anim_wins[0].navigator)
        self.anim_wins[0].board.bg_color = self.bg_color
        self.anim_wins[0].board.stroke_color = self.stroke_color
        self.anim_wins[0].board.stroke_weight = self.stroke_weight

    def save_ogn(self, title):
        """ Save a .ogn file

        it saves the first animation of self.anims"""
        self.rec.save_animation(self.anims[0], title)

    def export(self):
        """ Export frames to png

        Export frames of the first animation of self.anims"""
        self.rec.save_all_cells(root.anims[0])


# create application
root = Ognon()

if __name__ == '__main__':
    # create env
    root.n_anims_env(env, live=live)

    # tkinter main loop
    def secondloop():
        root.clock_win.clock.do_what_you_must_do()
        root.after(1, secondloop)
    if osc_sync:
        secondloop()
    root.mainloop()
    if root.clock_win.clock.server :
        root.clock_win.clock.server.shutdown()
