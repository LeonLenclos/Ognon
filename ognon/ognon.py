#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Ognon is a a software application for the creation of 2D animation
Ognon est un logiciel pour la création d'animation 2D

"""
from tkinter import *
from tkinter.ttk import *

from navigator import *
from board import *
from command_board import *

from settings import *


class Ognon(Tk):
    """L'application"""
    def __init__(self):
        super().__init__()
        self.geometry("{}x{}".format(self.winfo_screenwidth(), self.winfo_screenheight()-100))
        self.title("Ognon")

        self.anim = Animation(200, 200)
        self.navig = Navigator(self)

        self.board = Board(self)
        self.board.pack(pady=10)

        self.command_board = CommandBoard(self)
        self.command_board.pack(side=BOTTOM, pady=10)

if __name__ == '__main__':
    root = Ognon()
    root.mainloop()
