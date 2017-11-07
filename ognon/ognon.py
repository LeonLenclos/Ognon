#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Ognon is a a software application for the creation of 2D animation
Ognon est un logiciel pour la création d'animation 2D

"""

import tkinter as tk
#from tkinter import ttk

from interface import board, button_table, drawing_board, time_line
from control import navigator, operation, organizer, recorder


class Ognon(tk.Tk):
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
        self.recorder = recorder.Recorder(self)

        # On affiche le logo Ognon
        self.logo = tk.BitmapImage(file="resources/logo.xbm")
        self.logo_label = tk.Label(self, image=self.logo)
        self.logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # On cree deux boutons pour commencer
        self.button_table = button_table.ButtonTable(self)
        self.button_table.pack(side=tk.BOTTOM, pady=10)
        new_o = operation.Operation.dic['control.recorder']['new_ognon']
        open_o = operation.Operation.dic['control.recorder']['open_ognon']
        new_o.target = self.recorder
        open_o.target = self.recorder
        self.button_table.add_button('new_ognon', new_o)
        self.button_table.add_button('open_ognon', open_o)

        self.load_menu()

    def load(self, anim):
        """permet de charger une nouvelle anim"""
        #on supprime tous les widget
        for child in self.winfo_children():
            child.destroy()

        #on reinitialise les machines
        self.animation = anim
        self.navigator = navigator.Navigator(self.animation)
        self.organizer = organizer.Organizer(self.navigator)
        self.recorder = recorder.Recorder(self)

        # on cree un board
        self.board = drawing_board.DrawingBoard(self)
        self.board.add_navigator(self.navigator)
        self.board.pack(fill="both", expand=1)

        # on cree un deuxième board
        # self.alt_board_win = Toplevel()
        # self.alt_board_win.title("Ognon Live")
        # self.alt_board_win.geometry("{}x{}".format(300, 300))
        # self.alt_board = Board(self.alt_board_win, animation=self.animation, navigator=self.navigator)
        # self.alt_board.pack(fill="both", expand=1)

        # on cree le tableau de commande et la timeline
        self.button_table = button_table.ButtonTable(self)
        self.button_table.pack(side=tk.BOTTOM)  # , pady=10)
        self.time_line = time_line.TimeLine(self, self.navigator)
        self.time_line.pack(side=tk.BOTTOM)  # , pady=10)

        # on cree les boutons et le menu
        self.shortcuts = dict()
        operations = operation.Operation.dic
        for m in operations:
            if m == 'control.navigator':
                target = self.navigator
            elif m == 'control.organizer':
                target = self.organizer
            elif m == 'control.recorder':
                target = self.recorder
            for o in operations[m]:
                op = operations[m][o]
                op.target = target
                self.shortcuts[op.shortcut] = op
                self.bind_all("<KeyPress>".format(op.shortcut), self.shortcut)
                self.button_table.add_button(o, op)
        self.load_menu()

    def shortcut(self, event):
        if event.keysym in self.shortcuts:
            self.shortcuts[event.keysym]()

    def load_menu(self):
        self.menubar = tk.Menu(self)
        self.sub_menu = dict()
        self.shortcuts = dict()
        operations = operation.Operation.dic
        for m in operations:
            if m == 'control.navigator':
                target = self.navigator
            elif m == 'control.organizer':
                target = self.organizer
            elif m == 'control.recorder':
                target = self.recorder
            self.sub_menu[m] = tk.Menu(self.menubar)
            for o in operations[m]:
                op = operations[m][o]
                op.target = target
                self.shortcuts[op.shortcut] = op
                self.sub_menu[m].add_command(label=op.name, command=op)
            self.menubar.add_cascade(label=m, menu=self.sub_menu[m])
        self.config(menu=self.menubar)

if __name__ == '__main__':
    root = Ognon()
    root.mainloop()
