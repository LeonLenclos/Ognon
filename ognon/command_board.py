# -*-coding:Utf-8 -*

"""
This module is for the drawing canvas.

"""
from tkinter import *
import os
import re
# from tkinter.ttk import *


class CommandBoard(Frame):
    """C'est là où on dessine

    C'est un objet qui hérite de tkinter.Frame et qui cree un tkinter.canvas"""

    def __init__(self, parent):
        """Constructeur du board.

        on y innitialise les variables et evenements qui servent au dessin"""

        super().__init__(master=parent)
        self.anim = parent.animation
        self.nav = parent.navigator

        self.icns = {}
        for f in os.listdir("icns"):
            if re.search(r'.+\.xbm', f):
                self.icns[f] = BitmapImage(file="icns/"+f)
        #
        self.cells_pack = Frame(self)
        self.cells_pack.pack()

        # On crée les boutons
        self.buttons_pack = Frame(self)
        self.buttons_pack.pack()
        # LittleButton(self.buttons_pack, img="add_cell_before", command=lambda e: self.board.add_cell_before(), r=1)
        # LittleButton(self.buttons_pack, img="add_cell_after", command=lambda e: self.board.add_cell_after(), r=1)
        # LittleButton(self.buttons_pack, img="clone_cell_after", command=lambda e: self.board.clone_cell(), r=1)
        # LittleButton(self.buttons_pack, img="copy_cell_after", command=lambda e: self.board.copy_cell(), r=1)
        # LittleButton(self.buttons_pack, img="del_cell", command=lambda e: self.board.del_cell(), r=1)
        # LittleButton(self.buttons_pack, img="del_cell_content", command=lambda e: self.board.clear_cell(), r=1)
        # LittleButton(self.buttons_pack, img="move_cell_before", command=lambda e: self.board.move_cell_backward(), r=1)
        # LittleButton(self.buttons_pack, img="move_cell_after", command=lambda e: self.board.move_cell_forward(), r=1)
        # LittleButton(self.buttons_pack, img="prev_cell", command=lambda e: self.board.prev_cell(), r=1)
        # LittleButton(self.buttons_pack, img="next_cell", command=lambda e: self.board.next_cell(), r=1)
        # LittleButton(self.buttons_pack, img="first_cell", command=lambda e: self.board.go_to_first_cell(), r=1)
        # LittleButton(self.buttons_pack, img="last_cell", command=lambda e: self.board.go_to_last_cell(), r=1)
        # LittleButton(self.buttons_pack, img="play", command=lambda e: self.board.play(), r=1)
        self.cells_buttons = []

        # On reset une première fois
        self.reset()

    def add_button(self, img, command):
        LittleButton(self.buttons_pack, img=img, command=lambda e: command(), r=1)

    def reset(self):
        # On détruits tous les cells buttons
        for button in self.cells_buttons:
            button.destroy()
        LittleButton.column_index_of_raw[0] = -1

        # On recrée un bouton par cell
        i = 0
        for cell in self.anim:
            icone = 'cell'
            if i == self.nav.cursor:
                if cell.occurrences > 1:
                    icone += "_clone"
                icone += "_select"
            elif cell is self.nav.current_cell():
                icone += "_clone"
            self.cells_buttons.append(LittleButton(
                self.cells_pack, img=icone,
                command=lambda e: self.nav.go_to_cell(e.widget.id),
                r=0, id=i))
            i += 1


class LittleButton(Label):
    column_index_of_raw = {}

    def __init__(self, master, img="none", command=None, r=0, id=0, text=""):
        super().__init__(master)
        self.icn = master.master.icns[img + ".xbm"] if img + ".xbm" in master.master.icns else master.master.icns["none.xbm"]
        self.config(image=self.icn, width=self.icn.width(), height=self.icn.height(), borderwidth=2, relief=RAISED)
        self.id = id
        if r in LittleButton.column_index_of_raw:
            LittleButton.column_index_of_raw[r] += 1
        else:
            LittleButton.column_index_of_raw[r] = 0
        self.pack(side=LEFT)
        self.bind("<Button 1>", command)
