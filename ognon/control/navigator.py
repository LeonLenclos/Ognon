"""Provide a Navigator class to navigate into Animation"""

from control import operation as op


class Navigator():
    """Allow to navigate into one Animation."""
    def __init__(self, animation):
        self.anim = animation
        self._cursor = 0
        self.is_playing = False
        self.listeners = []
        # Pref
        self.play_in_loop = True

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = self.constrain_film_index(value)

    def add_listener(self, callback):
        self.anim.listeners.append(callback)
        self.listeners.append(callback)

    def reset(self):
        for l in self.listeners:
            l()

    def constrain_film_index(self, value):
        """Retourne une valeur contrainte entre 0 et la longueur de l'anim."""
        if self.play_in_loop:
            return value % len(self.anim)
        elif value >= len(self.anim):
            return len(self.anim) - 1
        elif value < 0:
            return 0
        else:
            return value

    def current_cell(self):
        self.cursor = self.cursor
        return self.anim[self.cursor]

    def current_onion_cells(self):
        if not self.is_playing:
            prev = self.constrain_film_index(self.cursor - 1)
            next = self.constrain_film_index(self.cursor + 1)
            if prev == next == self.cursor:
                return []
            elif prev == next:
                return [self.anim[prev]]
            else:
                return [self.anim[prev], self.anim[next]]

    def run(self):
        """Cette fonction s'occupe de la lecture de l'anim
        elle est appellée par play et n'est effective que si is_playing"""
        if self.is_playing:
            self.cursor += 1
            #self.parent.after(int(1000/settings["play speed"]), self.run)
            self.reset()

    ##############
    # OPERATIONS #
    ##############

    @op.operation(name="Play", shortcut="q")
    def play(self):
        """Permet de lire ou de stopper l'anim"""
        self.is_playing = not self.is_playing
        self.run()

    @op.operation(name="Image précédente", shortcut="z")
    def prev_cell(self):
        """Permet d'acceder à la cell précédente"""
        self.cursor -= 1
        self.reset()

    @op.operation(name="Image suivante", shortcut="s")
    def next_cell(self):
        """Permet d'acceder à la cell suivante"""
        self.cursor += 1
        self.reset()

    @op.operation(name="Première image", shortcut="e")
    def go_to_first_cell(self):
        """Permet d'acceder à la cell suivante"""
        self.cursor = 0
        self.reset()

    @op.operation(name="Dernière image", shortcut="d")
    def go_to_last_cell(self):
        """Permet d'acceder à la cell précédente"""
        self.cursor = len(self.anim)-1
        self.reset()

    @op.operation("int", name="Aller à telle image")
    def go_to_cell(self, i):
        """Permet d'acceder à une cell i"""
        self.cursor = i
        self.reset()
