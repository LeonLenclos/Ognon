# -*-coding:Utf-8 -*

"""
Ce module est pour le tableau de commande

"""
from tkinter import *
import os
import re
# from tkinter.ttk import *


class CommandBoard(Frame):
    """Un CommandBoard  est une Frame avec des LittleButtons"""

    def __init__(self, parent):
        super().__init__(master=parent)

        # Rangement boutons action
        self.buttons_pack = Frame(self)
        self.buttons_pack.pack()

    def add_button(self, img, command):
        return LittleButton(self.buttons_pack, img=img, command=lambda e: command())


class TimeLine(CommandBoard):
    """Une TimeLine est un CommandBoard un peu spécial"""

    def __init__(self, parent):
        super().__init__(parent)

        self.anim = parent.animation
        self.nav = parent.navigator

        # Rangement boutons cell
        self.cells_buttons = []
        self.specials_cells_buttons = []

        # On reset une première fois
        self.reset()

    def reset(self):
        # On détruits tous les cells buttons
        for button in self.cells_buttons:
            button.destroy()
        self.cells_buttons = []
        self.specials_cells_buttons = []

        # On recrée un bouton par cell
        i = 0
        for cell in self.anim:
            # on cherche les boutons speciaux pour les avoir sous la main lors de soft_reset si c'en est un track_it vaudra True a la fin
            track_it = True
            # on construit l'icone qu'il faut
            icone = 'cell'
            if i == self.nav.cursor:
                if cell.occurrences > 1:
                    icone += "_clone"
                icone += "_select"
            elif cell is self.nav.current_cell():
                icone += "_clone"
            else:
                track_it = False  # rien de spécial

            # on cree un  bouton
            new_button = LittleButton(
                self.buttons_pack, img=icone,
                command=lambda e: self.nav.go_to_cell(e.widget.id), id=i)

            # on le range dans cells_buttons
            self.cells_buttons.append(new_button)
            # on le ranfe dans specials_cells s'il faut
            if track_it:
                self.specials_cells_buttons.append(new_button)

            i += 1

    def soft_reset(self):
        #l'idée du soft reset est de ne pas etre trop lourd pour quand on en a pas besoin
        # donc au lieu de tout supprimer et de tout recreer comme dans le reset(),
        # on va juste changer les trucs qui ont changé

        #on ne fait ça que si la taille de l'anim n'a pas changé
        if len(self.anim) == len(self.cells_buttons):
            # on commence par donner une apparence normale à tous les boutons spéciaux
            for button in self.specials_cells_buttons:
                button.change_icn('cell')
            # on réinitialise la liste des boutons speciaux avec comme premier ellement le bouton de la current_cell
            self.specials_cells_buttons = []
            self.specials_cells_buttons.append(self.cells_buttons[self.nav.cursor])
            # si cette cell n'as pas de clone on lui donne l'apparence d'une cell_select
            if self.nav.current_cell().occurrences == 1:
                self.cells_buttons[self.nav.cursor].change_icn('cell_select')
            #si elle a des clones alors on lui donne l'apparence qu'il faut
            # et on va chercher tous ses clones pour leur donner l'apparence qu'il faut et les ranger dans les boutons speciaux
            else:
                self.cells_buttons[self.nav.cursor].change_icn('cell_clone_select')
                i = 0
                for cell in self.anim:
                    if cell is self.nav.current_cell() and not self.nav.cursor == i:
                        self.cells_buttons[i].change_icn('cell_clone')
                        self.specials_cells_buttons.append(self.cells_buttons[i])
                    i += 1


class LittleButton(Label):

    # on pourra acceder aux icones grace à LittleButton.icns["nom.xbm"]
    icns = {}

    def change_icn(self, img):
            """cette method permet de changer l'icn d'un bouton"""
            self.img = img
            # si le bouton existe on le met, sinon on met none.xbm
            icon = LittleButton.icns[self.img + ".xbm"] if self.img + ".xbm" in LittleButton.icns else LittleButton.icns["none.xbm"]
            self.config(image=icon)

    def __init__(self, master, img="none", command=None, id=0):
        """ id est utile pour les cell button, img doit etre le nom de l'icone sans l'extension, command est la fonction qui est appellée quand on clic sur le bouton"""
        super().__init__(master)

        # si LittleButton.icns n'est pas encore plein d'icones, on le rempli avec tout ce qu'on trouve
        icns = LittleButton.icns
        if len(icns) == 0:
            for f in os.listdir("icns"):
                if re.search(r'.+\.xbm', f):
                    icns[f] = BitmapImage(file="icns/"+f)

        self.id = id
        self.change_icn(img)
        self.bind("<Button 1>", command)
        self.pack(side=LEFT)
