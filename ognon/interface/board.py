# -*-coding:Utf-8 -*
"""Provide two classes for displaying or drawing on Animation.

Board -- Allow to display one or more Animation.
DrawingBoard -- Allow to display and draw on one Animation."""

import tkinter as tk
from control import pencil


class Board(tk.Frame):
    """Create an area for displaying one or more Animation.

    It subclasses tkinter.Frame and creates a tkinter.Canvas.
    It can be subclassed for more specifics kinds of boards like DrawingBoard
    After being created it must be linked to one or more Navigator
    """

    def __init__(self, parent):
        """Construct an empty Board."""
        super().__init__(parent)

        # Preferences
        self.show_onion = True
        self.bg_color = 'white'
        self.stroke_color = 'black'
        self.stroke_weight = 10

        self.nav = []

        self.canvas = tk.Canvas(self, cursor='pencil', width=10, height=10)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def add_navigator(self, nav):
        """Link the board to a Navigator."""
        self.nav.append(nav)
        # Ask for the navigator to reset this Board when something move in
        # the Animation or in the Navagitor.
        nav.add_listener(self.reset)
        # For now, board dimensions are fixed from the last Navigator added.
        self.canvas.config(width=nav.anim.width, height=nav.anim.height)

    def reset(self):
        """Redraw the Board's content.

        Must be call when something move in linked Animation or Navagitor."""
        self.canvas.config(bg=self.bg_color)

        self.canvas.delete("all")
        # on affiche la current frm de chaque nav.
        for n in self.nav:
            self.draw_onion(n.current_onion_cells())
            self.draw_cell(n.current_cell(), fill=self.stroke_color)

    def draw_cell(self, cell, fill="black"):
        """Draw the passed cell in the Board"""
        for l in cell.lines:
            options = {"fill": fill,
                       "width": self.stroke_weight}
            self.canvas.create_line(tuple(l), options)

    def draw_onion(self, cells):
        # On affiche la pelure d'oninon s'il faut cells est un tuple avec 0 ou 1 ou 2 cells
        if self.show_onion and cells is not None:
            fill_color = "red3"
            for c in cells:
                self.draw_cell(c, fill=fill_color)
                fill_color = "green4"


class DrawingBoard(Board):
    """C'est là où on dessine
    C'est un objet qui hérite de Board"""

    def __init__(self, parent):
        """Constructeur du board.
        on y innitialise les variables et evenements qui servent au dessin"""
        super().__init__(parent)
        # Le crayon
        self.pencil = pencil.Pencil()
        # Les evenements qui font le dessin
        self.canvas.bind('<Button>', self._start_drawing)
        self.canvas.bind('<ButtonRelease>', self._stop_drawing)
        self.canvas.bind('<Motion>', self._keep_drawing)

        # Boléens qui disent si on est en train de dessiner ou d'effacer
        self.is_drawing = False
        self.is_erasing = False
        # Là où on stock les coordonées de la ligne que l'on dessine
        self.line_coords = []

    def _start_drawing(self, event):
        """Cette fonction commence le trait"""
        # On commence la ligne
        self.line_coords = [event.x, event.y]

        if event.num == 1:
            self.is_drawing = True
        else :
            self.is_erasing = True

    def _stop_drawing(self, event):
        """Cette fonction termine le trait"""
        # On envoie les infos au pencil
        self.pencil.save_line()
        # On annonce que le trait est fini
        self.is_drawing = self.is_erasing = False

    def _keep_drawing(self, event):
        """Cette fonction dessine le trait"""
        if self.is_drawing or self.is_erasing:
            # On garde en mémoire les coordonnées du point
            self.line_coords.append(event.x)
            self.line_coords.append(event.y)
            # On envoie les infos au pencil
            if self.is_drawing:
                self.pencil.draw_tmp_line(self.line_coords, self.nav[0].current_cell())
            else:
                self.pencil.erase(self.line_coords, self.nav[0].current_cell())