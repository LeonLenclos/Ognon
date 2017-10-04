from settings import *
from operation import *


class Navigator():
    """docstring for Navigator"""
    def __init__(self, parent):
        self.parent = parent
        self.anim = self.parent.anim
        self._cursor = 0

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
        pass

    ##############
    # OPERATIONS #
    ##############

    @Operation
    def go_to_frm(self, i):
        """Permet d'acceder à une frm i"""
        self.cursor = i
        self.reset()

    @Operation
    def next_frm(self):
        """Permet d'acceder à la frm suivante"""
        self.cursor += 1
        self.reset()

    @Operation
    def prev_frm(self):
        """Permet d'acceder à la frm précédente"""
        self.cursor -= 1
        self.reset()

    @Operation
    def go_to_first_frm(self):
        """Permet d'acceder à la frm suivante"""
        self.cursor = 0
        self.reset()

    @Operation
    def go_to_last_frm(self):
        """Permet d'acceder à la frm précédente"""
        self.cursor = len(self.anim)-1
        self.reset()

    @Operation
    def run(self):
        """Cette fonction s'occupe de la lecture de l'anim
        elle est appellée par play et n'est effective que si is_playing"""
        if self.is_playing:
            self.cursor += 1
            self.after(int(1000/settings["play speed"]), self.run)
            self.reset()

    @Operation
    def play(self):
        """Permet de lire ou de stopper l'anim"""
        self.is_playing = not self.is_playing
        self.run()