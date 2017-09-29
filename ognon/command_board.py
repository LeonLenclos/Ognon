# -*-coding:Utf-8 -*

"""
This module is for the drawing canvas.

"""
from tkinter import *
import os
import re
# from tkinter.ttk import *


class CommandBoard(Toplevel):
    """C'est là où on dessine

    C'est un objet qui hérite de tkinter.Frame et qui cree un tkinter.canvas"""

    def __init__(self, board):
        """Constructeur du board.

        on y innitialise les variables et evenements qui servent au dessin"""

        super().__init__(master=board)
        self.board = board

        # On règle les dimensions
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        wh = 50
        self.geometry("{}x{}+{}+{}".format(sw-10, wh, 5, sh-wh-5))
        self.resizable(width=False, height=False)
        self.title("Ognon's Command Board")
        # On importe les icones
        self.icns = {}
        for f in os.listdir("icns"):
            if re.search(r'.+\.xbm', f):
                self.icns[f] = BitmapImage(file="icns/"+f)
        #
        self.frms_pack = Frame(self)
        self.frms_pack.pack()

        # On crée les boutons
        self.buttons_pack = Frame(self)
        self.buttons_pack.pack()
        LittleButton(self.buttons_pack, img="add_frm_before", command=lambda e: self.board.add_frm_before(), r=1)
        LittleButton(self.buttons_pack, img="add_frm_after", command=lambda e: self.board.add_frm_after(), r=1)
        LittleButton(self.buttons_pack, img="clone_frm_after", command=lambda e: self.board.clone_frm(), r=1)
        LittleButton(self.buttons_pack, img="copy_frm_after", command=lambda e: self.board.copy_frm(), r=1)
        LittleButton(self.buttons_pack, img="del_frm", command=lambda e: self.board.del_frm(), r=1)
        LittleButton(self.buttons_pack, img="del_frm_content", command=lambda e: self.board.clear_frm(), r=1)
        LittleButton(self.buttons_pack, img="move_frm_before", command=lambda e: self.board.move_frm_backward(), r=1)
        LittleButton(self.buttons_pack, img="move_frm_after", command=lambda e: self.board.move_frm_forward(), r=1)
        LittleButton(self.buttons_pack, img="prev_frm", command=lambda e: self.board.prev_frm(), r=1)
        LittleButton(self.buttons_pack, img="next_frm", command=lambda e: self.board.next_frm(), r=1)
        LittleButton(self.buttons_pack, img="first_frm", command=lambda e: self.board.go_to_first_frm(), r=1)
        LittleButton(self.buttons_pack, img="last_frm", command=lambda e: self.board.go_to_last_frm(), r=1)
        LittleButton(self.buttons_pack, img="play", command=lambda e: self.board.play(), r=1)
        self.frms_buttons = []

        # On reset une première fois
        self.reset()

    def reset(self):
        # On détruits tous les frms buttons
        for button in self.frms_buttons:
            button.destroy()
        LittleButton.column_index_of_raw[0] = -1

        # On recrée un bouton par frm
        i = 0
        for frm in self.board.animation:
            icone = 'frm'
            if i == self.board.cursor:
                if frm.occurrences > 1:
                    icone += "_clone"
                icone += "_select"
            elif frm is self.board.current_frm:
                icone += "_clone"
            self.frms_buttons.append(LittleButton(
                self.frms_pack, img=icone,
                command=lambda e: self.board.go_to_frm(e.widget.id),
                r=0, id=i))
            i += 1


class LittleButton(Label):
    column_index_of_raw = {}

    def __init__(self, master, img="none", command=None, r=0, id=0, text=""):
        super().__init__(master)
        self.icn = master.master.icns[img + ".xbm"]
        print(self.icn)
        self.config(image=self.icn, width=self.icn.width(), height=self.icn.height())
        self.id = id
        if r in LittleButton.column_index_of_raw:
            LittleButton.column_index_of_raw[r] += 1
        else:
            LittleButton.column_index_of_raw[r] = 0
        self.pack(side=LEFT)
        self.bind("<Button 1>", command)
