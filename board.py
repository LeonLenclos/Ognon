# -*-coding:Utf-8 -*

"""
Ce module est pour la fenetre principale : Board
On y définie la class Board qui hérite de tkinter.Tk
"""
from tkinter import *
from tkinter import filedialog
import PIL.Image
import PIL.ImageDraw

from animation import *
from command_board import *
from settings import *


class Board(Tk):
    """C'est là où on dessine

    C'est un objet qui hérite de tkinter.Tk et qui cree un tkinter.canvas"""

    def __init__(self, w, h):
        """Constructeur du board.

        on y innitialise les variables et evenements qui servent au dessin"""
        super().__init__()

        #Taille et apparence de la fenetre
        self.w = w
        self.h = h
        self.geometry("{}x{}".format(self.w+20, self.h+20))
        self.resizable(width=False, height=False)
        self.configure(background='PeachPuff3')
        self.title("Ognon's Board")
        # Création du Canvas
        self.canvas = Canvas(self, width=w, height=h, cursor='pencil')
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        # Les evenements qui font le dessin
        self.canvas.bind('<Button 1>', self._start_drawing)
        self.canvas.bind('<ButtonRelease 1>', self._stop_drawing)
        self.canvas.bind('<Motion>', self._keep_drawing)
        # Là où est la souris au moment -1
        self.p_mouse_x = 0
        self.p_mouse_y = 0
        # Boléens qui disent si on est en train de dessiner et de jouer l'animation
        self.is_drawing = False
        self.is_playing = False
        # Là où on stock les coordonées de la ligne que l'on dessine
        self.current_line_coord = []
        # On cree le cursor
        self._cursor = 0
        # on cree l'animation et une premiere frm qu'on memorise dans current_frm
        self.animation = Animation()
        self.current_frm = self.animation[self.cursor]
        # On cree le tableau de commande
        self.command_board = CommandBoard(self)

    def constrain_film_index(self, value, loop=settings["play in loop"]):
        """Retourne une valeur contrainte entre 0 et la longueur de l'animation."""
        if loop:
            return value % len(self.animation)
        elif value >= len(self.animation):
            return len(self.animation) - 1
        elif value < 0:
            return 0
        else:
            return value

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = self.constrain_film_index(value)

    def save_all_frames(self):
        directory = filedialog.askdirectory() + "/"
        i = 0
        for frm in self.animation:
            self.save_frame(frm, directory + str(i).zfill(4) + ".png")
            i += 1

    def save_frame(self, frm, path):
        img = PIL.Image.new("RGB", (self.w, self.h), 'white')
        draw = PIL.ImageDraw.Draw(img)
        for line in frm.lines:
            draw.line(line, 'black')
        img.save(path)

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
        #    self.canvas.create_line(tuple(self.current_line_coord))
        # On ajoure les coordonnees de la ligne a la current_frm
            self.current_frm.add_line(self.current_line_coord)
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

    def navigation(fun):
        """a chaque fois qu'on navigue on appellera ça"""
        def do_it_and_reset_current_frm(*args, **kwargs):
            ret = fun(*args, **kwargs)
            self = args[0]
            self.cursor = self.cursor  # au cas ou out of range.
            self.current_frm = self.animation[self.cursor]
            self.reset()
            return ret
        return do_it_and_reset_current_frm

    @navigation
    def go_to_frm(self, i):
        """Permet d'acceder à une frm i"""
        self.cursor = i

    @navigation
    def next_frm(self):
        """Permet d'acceder à la frm suivante"""
        self.cursor += 1

    @navigation
    def prev_frm(self):
        """Permet d'acceder à la frm précédente"""
        self.cursor -= 1

    @navigation
    def go_to_first_frm(self):
        """Permet d'acceder à la frm suivante"""
        self.cursor = 0

    @navigation
    def go_to_last_frm(self):
        """Permet d'acceder à la frm précédente"""
        self.cursor = len(self.animation)-1

    @navigation
    def add_frm_after(self):
        """Permet d'ajouter une frm après l'actuelle"""
        self.animation.add_frm(self.cursor+1)
        self.next_frm()

    @navigation
    def add_frm_before(self):  # PAS ENCORE EN MARCHE
        """Permet d'ajouter une frm avant l'actuelle"""
        self.animation.add_frm(self.cursor)

    @navigation
    def clone_frm(self):
        """Permet de supprimer la frm actuelle"""
        self.animation.clone_frm(self.cursor)
        self.next_frm()

    @navigation
    def move_frm_forward(self):
        """Permet de supprimer la frm actuelle"""
        self.animation.move_frm_to(self.cursor, self.cursor + 1)
        self.next_frm()

    @navigation
    def move_frm_backward(self):
        """Permet de supprimer la frm actuelle"""
        self.animation.move_frm_to(self.cursor, self.cursor - 1)
        self.prev_frm()

    @navigation
    def copy_frm(self):
        """Permet de supprimer la frm actuelle"""
        self.animation.copy_frm(self.cursor)
        self.move_frm_forward()

    @navigation
    def del_frm(self):
        """Permet de supprimer la frm actuelle"""
        self.animation.del_frm(self.cursor)
        self.prev_frm()

    def clear_frm(self):
        """Permet d'effacer la frm actuelle"""
        self.current_frm.clear()
        self.reset()

    def play(self):
        """Permet de lire ou de stopper l'animation"""
        self.is_playing = not self.is_playing
        self.run()

    @navigation
    def run(self):
        """Cette fonction s'occupe de la lecture de l'animation
        elle est appellée par play et n'est effective que si is_playing"""
        if self.is_playing:
            self.cursor += 1
            self.after(int(1000/settings["play speed"]), self.run)

    def onion(self):
        # On affiche la pelure d'oninon s'il faut
        if not self.is_playing and settings["onion skinning show"]:
            prev_index = self.constrain_film_index(
                self.cursor - settings["onion skinning range"],
                loop=settings["onion skinning loop"])
            next_index = self.constrain_film_index(
                self.cursor + settings["onion skinning range"],
                loop=settings["onion skinning loop"])
            if self.animation[prev_index] is not self.current_frm:
                for l in self.animation[prev_index].lines:
                    self.canvas.create_line(tuple(l), fill="tomato")
            if self.animation[next_index] is not self.current_frm and self.animation[next_index] is not self.animation[prev_index]:
                for l in self.animation[next_index].lines:
                    self.canvas.create_line(tuple(l), fill="aquamarine")

    def reset(self):
        """Cette fonction doit être appellé dès qu'il y a modification
        pour actualiser l'affichage de la fenetre"""
        # On commence par tout effacer
        self.canvas.delete("all")
        # On affiche le contenu de current_frm
        self.onion()
        for l in self.current_frm.lines:
            self.canvas.create_line(tuple(l), activedash=[1, 1])
        # on appelle aussi le reset du commandboard
        self.command_board.reset()
