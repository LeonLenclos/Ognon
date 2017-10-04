from settings import *
from operation import *


class Navigator():
    """docstring for Navigator"""
    def __init__(self, parent):
        self.parent = parent
        self.anim = parent.animation
        self._cursor = 0
        self.is_playing = False

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = self.constrain_film_index(value)

    def constrain_film_index(self, value, loop=settings["play in loop"]):
        """Retourne une valeur contrainte entre 0 et la longueur de l'anim."""
        if loop:
            return value % len(self.anim)
        elif value >= len(self.anim):
            return len(self.anim) - 1
        elif value < 0:
            return 0
        else:
            return value

    def reset(self):
        self.parent.reset()

    def current_cell(self):
        return self.anim[self.cursor]

    def run(self):
        """Cette fonction s'occupe de la lecture de l'anim
        elle est appellée par play et n'est effective que si is_playing"""
        if self.is_playing:
            self.cursor += 1
            self.parent.after(int(1000/settings["play speed"]), self.run)
            self.reset()

    ##############
    # OPERATIONS #
    ##############

    @operation(int, name="Aller à telle image", shortcut="/")
    def go_to_cell(self, i):
        """Permet d'acceder à une cell i"""
        self.cursor = i
        self.reset()

    @operation(name="Image suivante", shortcut=".")
    def next_cell(self):
        """Permet d'acceder à la cell suivante"""
        self.cursor += 1
        self.reset()

    @operation(name="Image précédente", shortcut=",")
    def prev_cell(self):
        """Permet d'acceder à la cell précédente"""
        self.cursor -= 1
        self.reset()

    @operation(name="Première image", shortcut="Shift_,")
    def go_to_first_cell(self):
        """Permet d'acceder à la cell suivante"""
        self.cursor = 0
        self.reset()

    @operation(name="Dernière image", shortcut="Shift_.")
    def go_to_last_cell(self):
        """Permet d'acceder à la cell précédente"""
        self.cursor = len(self.anim)-1
        self.reset()

    @operation(name="Play", shortcut=" ")
    def play(self):
        """Permet de lire ou de stopper l'anim"""
        self.is_playing = not self.is_playing
        self.run()
