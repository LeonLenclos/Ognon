from settings import *
from operation import *


class Organizer():
    """docstring for Navigator"""
    def __init__(self, parent):
        self.parent = parent
        self.anim = parent.animation
        self.nav = parent.navigator

    def reset(self):
        self.parent.reset()

    ##############
    # OPERATIONS #
    ##############

    @operation(name="Ajouter une image après", shortcut="]")
    def add_cell_after(self):
        self.anim.add_cell(self.nav.cursor+1)
        self.nav.next_cell()
        self.reset()

    @operation(name="Ajouter une image avant", shortcut="[")
    def add_cell_before(self):
        self.anim.add_cell(self.nav.cursor)
        self.reset()

    @operation(name="Cloner l'image", shortcut="=")
    def clone_cell(self):
        self.anim.clone_cell(self.nav.cursor)
        self.nav.next_cell()
        self.reset()

    @operation(name="Déplacer l'image en avant", shortcut="Shift_]")
    def move_cell_forward(self):
        self.anim.move_cell_to(self.nav.cursor, self.nav.cursor + 1)
        self.nav.next_cell()
        self.reset()

    @operation(name="Déplacer l'image en arrière", shortcut="Shift_[")
    def move_cell_backward(self):
        self.anim.move_cell_to(self.nav.cursor, self.nav.cursor - 1)
        self.nav.prev_cell()
        self.reset()

    @operation(name="Copier l'image", shortcut="Shift_=")
    def copy_cell(self):
        self.anim.copy_cell(self.nav.cursor)
        self.move_cell_forward()
        self.reset()

    @operation(name="Suprimer l'image", shortcut="-")
    def del_cell(self):
        self.anim.del_cell(self.nav.cursor)
        self.nav.prev_cell()
        self.reset()
