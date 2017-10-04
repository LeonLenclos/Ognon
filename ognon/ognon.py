#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Ognon is a a software application for the creation of 2D animation
Ognon est un logiciel pour la création d'animation 2D

"""
from tkinter import *
from tkinter.ttk import *

from animation import *
from navigator import *
from organizer import *
from recorder import *
from board import *
from command_board import *

from settings import *
from operation import *


class Ognon(Tk):
    """L'application"""
    def __init__(self):
        super().__init__()
        self.geometry("{}x{}".format(self.winfo_screenwidth(), self.winfo_screenheight()-100))
        self.title("Ognon")

        self.animation = Animation(200, 200)
        self.navigator = Navigator(self)
        self.organizer = Organizer(self)
        self.recorder = Recorder(self)

        self.board = Board(self)
        self.board.pack(pady=10)

        self.command_board = CommandBoard(self)
        self.command_board.pack(side=BOTTOM, pady=10)

        menu_bar = Menu(self)
        for m in Operation.dic:
            menu = Menu(menu_bar, tearoff=0)
            if m == 'navigator':
                target = self.navigator
            elif m == 'organizer':
                target = self.organizer
            elif m == 'recorder':
                target = self.recorder
            for o in Operation.dic[m]:
                op = Operation.dic[m][o]
                op.target = target
                menu.add_command(label=op.name, command=Operation.dic[m][o])
                self.command_board.add_button(o, Operation.dic[m][o])
            menu_bar.add_cascade(label=m, menu=menu)
        self.config(menu=menu_bar)

    def reset(self):
        self.board.reset()
        self.command_board.reset()

if __name__ == '__main__':
    root = Ognon()
    root.mainloop()
