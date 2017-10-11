# -*-coding:Utf-8 -*
from tkinter import *

from settings import *


class Board(Frame):
    """C'est là où on dessine
    C'est un objet qui hérite de Frame et qui cree un canvas"""

    def __init__(self, parent):
        """Constructeur du board.
        on y innitialise les variables et evenements qui servent au dessin"""
        super().__init__(parent)
        # on recup l'anim et une premiere cell qu'on memorise dans current_cell
        self.anim = self.master.animation
        self.nav = self.master.navigator
        # Création du Canvas
        self.canvas = Canvas(self, width=self.anim.width, height=self.anim.height, borderwidth=1, relief=RIDGE, cursor='pencil')
        self.canvas.pack()
        # Les evenements qui font le dessin
        self.canvas.bind('<Button 1>', self._start_drawing)
        self.canvas.bind('<ButtonRelease 1>', self._stop_drawing)
        self.canvas.bind('<Motion>', self._keep_drawing)
        self.canvas.bind_all('<BackSpace>', self._erase)
        # Là où est la souris au moment -1
        self.p_mouse_x = 0
        self.p_mouse_y = 0
        # Boléens qui disent si on est en train de dessiner
        self.is_drawing = False
        # Là où on stock les coordonées de la ligne que l'on dessine
        self.current_line_coord = []
        # On cree le tableau de commande
        # self.command_board = CommandBoard(self)

    def _start_drawing(self, event):
        """Cette fonction commence le trait"""
        # On réinnitialise les variables
        self.p_mouse_x = event.x
        self.p_mouse_y = event.y
        self.current_line_coord = []
        # On annonce que le dessin est en cours
        self.is_drawing = True

    def _stop_drawing(self, event):
        """Cette fonction termine le trait"""
        # On suprime le dessin temporaire
        self.canvas.delete("tmp")
        # S'il y a eu un dessin on le recrée et le stock dans current_line_coord
        if len(self.current_line_coord) >= 4:
            # On ajoure les coordonnees de la ligne a la current_cell
            self.nav.current_cell().add_line(self.current_line_coord)
        self.reset()
        # On annonce que le dessin est fini
        self.is_drawing = False

    def _keep_drawing(self, event):
        """Cette fonction dessine le trait"""
        if self.is_drawing:
            # On garde en mémoire les coordonnées du point où l'on
            # est pour pouvoir ne faire qu'une seule ligne à la fin
            self.current_line_coord.append(self.p_mouse_x)
            self.current_line_coord.append(self.p_mouse_y)
            # On trace une ligne temporaire entre le point où l'on
            # est et le point précédent (elle sera effacée à la fin)
            self.canvas.create_line(
                self.p_mouse_x, self.p_mouse_y,
                event.x, event.y,
                tags="tmp")
            # On actualise les coordonnées du "point précédent"
            self.p_mouse_x = event.x
            self.p_mouse_y = event.y

    def _erase(self, event):
        """Cette fonction efface un trait"""
        if not self.is_drawing:
            # on récupere l'id de l'ellement sous la souris
            id_to_del = self.canvas.find_withtag(CURRENT)[0]
            # on récupère les tags de cet element -> ["l4", "current"] (par exemple, pour la 4ème ligne)
            # on prend le premier tag -> "l4"
            # on enlève le premier caractère -> "4"
            # on transforme en int -> 4
            line_to_del = int(self.canvas.gettags(id_to_del)[0][1:])
            # on suprime la ligne directement dans la liste lines de la current_cell
            del self.nav.current_cell().lines[line_to_del]
            # on reset
            self.reset()

    def onion(self):
        # On affiche la pelure d'oninon s'il faut
        if not self.nav.is_playing and settings["onion skinning show"]:
            prev_index = self.nav.constrain_film_index(
                self.nav.cursor - settings["onion skinning range"],
                loop=settings["onion skinning loop"])
            next_index = self.nav.constrain_film_index(
                self.nav.cursor + settings["onion skinning range"],
                loop=settings["onion skinning loop"])
            if self.anim[prev_index] is not self.nav.current_cell():
                for l in self.anim[prev_index].lines:
                    self.canvas.create_line(tuple(l), fill="tomato")
            if self.anim[next_index] is not self.nav.current_cell() and self.anim[next_index] is not self.anim[prev_index]:
                for l in self.anim[next_index].lines:
                    self.canvas.create_line(tuple(l), fill="aquamarine")

    def reset(self):
        """Cette fonction doit être appellé dès qu'il y a modification
        pour actualiser l'affichage de la fenetre"""
        # On commence par tout effacer
        self.canvas.delete("all")
        # On affiche l'onion
        self.onion()
        # On affiche le contenu de current_cell
        i = 0
        for l in self.nav.current_cell().lines:
            #on donne le tag "l{i}" pour pouvoir retrouver les lignes (cf: _erease())
            self.canvas.create_line(tuple(l), activedash=[1, 1], tag="l{}".format(i))
            i += 1
