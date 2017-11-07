# -*-coding:Utf-8 -*
import tkinter as tk


class Board(tk.Frame):
    """
    C'est un objet qui hérite de tk.Frame et qui cree un canvas"""

    def __init__(self, parent):
        """Constructeur du board."""
        super().__init__(parent)
        # la list qui contient les nav affichées ici
        self.nav = []
        # prefs
        self.show_onion = True
        self.stroke_weight = 2
        # style
        self.config(bg='black')
        # Création du Canvas
        self.canvas = tk.Canvas(self, cursor='pencil', width=10, height=10)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def add_navigator(self, nav):
        """cette fonction ajoute un navigator au board"""
        self.nav.append(nav)
        nav.add_listener(self.reset)
        self.canvas.config(width=nav.anim.width, height=nav.anim.height)

    def reset(self):
        """Cette fonction doit être appellé dès qu'il y a modification
        pour actualiser l'affichage de la fenetre"""
        # On commence par tout effacer
        self.canvas.delete("all")
        # on affiche la current frm de chaque nav
        for n in self.nav:
            self.draw_cell(n.current_cell())
            self.draw_onion(n.current_onion_cells())

    def draw_cell(self, cell, fill="black", erasable=False):
        i = 0
        for l in cell.lines:
            options = {"fill": fill,
                       "width": self.stroke_weight}
            if erasable:
                #on donne le tag "l{i}" pour pouvoir retrouver les lignes (cf: _erease())
                options["tag"] = "l{}".format(i)
                options["activedash"] = [1, 1]
            self.canvas.create_line(tuple(l), options)
            i += 1

    def draw_onion(self, cells):
        # On affiche la pelure d'oninon s'il faut cells est un tuple avec 0 ou 1 ou 2 cells

        if self.show_onion:
            fill_color = "tomato"
            for c in cells:
                self.draw_cell(c, fill=fill_color)
                fill_color = "aquamarine"
