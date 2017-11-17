#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Ognon is a a software application for the creation of 2D animation
Ognon est un logiciel pour la création d'animation 2D

"""

import tkinter as tk
#from tkinter import ttk

from interface import board, win, table
from control import recorder


class Ognon(tk.Tk):
    """L'application"""
    def __init__(self):

        super().__init__()
        # Taille et titre de la fenêtre
        self.geometry("{}x{}".format(150, 150))
        self.title("Ognon")

        #innitialisation du rec
        self.rec = recorder.Recorder("/Document/OGNON/Animations")

        # On affiche le logo Ognon
        self.logo = tk.BitmapImage(file="resources/logo.xbm")
        self.logo_label = tk.Label(self, image=self.logo)
        self.logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        #TEST

if __name__ == '__main__':
    root = Ognon()
    root.mainloop()

 
def simple_env(root):
    anim = root.rec.new_animation()
    anim_win = win.AnimationWindow()
    anim_win.load(anim)
    clock_win = win.ClockWindow()
    clock_win.add_navigator(anim_win.navigator)


def n_anims_env(root, n):
    anims = []
    anim_wins = []
    live_win = win.BoardWindow()
    clock_win = win.ClockWindow()
    for i in range(n):
        anims.append(root.rec.new_animation())
        a = anims[i]
        w = win.AnimationWindow()
        w.load(a)
        anim_wins.append(w)
        live_win.add_navigator(w.navigator)
        clock_win.add_navigator(w.navigator)
