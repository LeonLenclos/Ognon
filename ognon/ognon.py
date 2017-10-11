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
        # Taille et titre de la fenêtre
        self.geometry("{}x{}".format(300, 300))
        self.title("Ognon")

        #innitialisation des machines
        self.animation = None
        self.navigator = None
        self.organizer = None
        self.recorder = Recorder(self)

        # On affiche le logo Ognon
        self.logo = BitmapImage(file="img/logo.xbm")
        self.logo_label = Label(self, image=self.logo)
        self.logo_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        # On cree deux boutons pour commencer
        self.command_board = CommandBoard(self)
        self.command_board.pack(side=BOTTOM, pady=10)
        new_o = Operation.dic['recorder']['new_ognon']
        open_o = Operation.dic['recorder']['open_ognon']
        new_o.target = self.recorder
        open_o.target = self.recorder
        self.command_board.add_button('new_ognon', new_o)
        self.command_board.add_button('open_ognon', open_o)

    def reset(self):
        """permet de reseter tout ce qui doit l'etre"""
        self.board.reset()
        self.time_line.reset()

    def reset_navig(self):
        """permet de reseter tout ce qui doit l'etre lorsque navig demande un reset"""
        self.board.reset()
        self.time_line.soft_reset()

    def load(self, animation):
        """permet de charger une nouvelle anim"""
        #on supprime tous les widget
        for child in self.winfo_children():
            child.destroy()

        #on reinitialise les machines
        self.animation = animation
        self.navigator = Navigator(self, self.reset_navig)
        self.organizer = Organizer(self)
        self.recorder = Recorder(self)

        # on cree un board
        self.board = Board(self)
        self.board.pack(pady=10)

        # on cree le tableau de commande et la timeline
        self.command_board = CommandBoard(self)
        self.command_board.pack(side=BOTTOM, pady=10)
        self.time_line = TimeLine(self)
        self.time_line.pack(side=BOTTOM, pady=10)

        # on cree les boutons
        self.shortcuts = dict()
        for m in Operation.dic:
            if m == 'navigator':
                target = self.navigator
            elif m == 'organizer':
                target = self.organizer
            elif m == 'recorder':
                target = self.recorder
            for o in Operation.dic[m]:
                op = Operation.dic[m][o]
                op.target = target
                print("fonction {}, shortcut : {}".format(op.name, op.shortcut))
                self.shortcuts[op.shortcut] = op
                self.bind_all("<KeyPress>".format(op.shortcut), self.shortcut)
                self.command_board.add_button(o, op)

        # on reset
        self.reset()

    def shortcut(self, event):
        self.shortcuts[event.keysym]()


if __name__ == '__main__':
    root = Ognon()
    root.mainloop()
