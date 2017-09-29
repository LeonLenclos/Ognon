#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Ognon is a a software application for the creation of 2D animation
Ognon est un logiciel pour la création d'animation 2D

"""
from tkinter import *
from tkinter.ttk import *

from board import *
from settings import *


#création de la fenetre et du board
board = Board(800, 600)

# Création du menu
menu_bar = Menu(board)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save Frames", command=board.save_all_frames)
file_menu.add_command(label="Settings", command=settings.edit)
menu_bar.add_cascade(label="Fichier", menu=file_menu)
board.config(menu=menu_bar)


#lancement de la boucle
board.mainloop()
