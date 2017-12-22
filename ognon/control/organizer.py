from control import operation as op


class Organizer():
    """docstring for Navigator"""
    def __init__(self, nav):
        self.nav = nav
        self.anim = self.nav.anim

    ##############
    # OPERATIONS #
    ##############

    @op.operation(name="Ajouter une image après", shortcut="f")
    def add_cell_after(self):
        self.anim.add_cell(self.nav.cursor+1)
        self.nav.next_cell()

    @op.operation(name="Ajouter une image avant", shortcut="r")
    def add_cell_before(self):
        self.anim.add_cell(self.nav.cursor)

    @op.operation(name="Déplacer l'image en avant", shortcut="j")
    def move_cell_forward(self):
        self.anim.move_cell_to(self.nav.cursor, self.nav.cursor + 1)
        self.nav.next_cell()

    @op.operation(name="Déplacer l'image en arrière", shortcut="u")
    def move_cell_backward(self):
        self.anim.move_cell_to(self.nav.cursor, self.nav.cursor - 1)
        self.nav.prev_cell()

    @op.operation(name="Copier l'image", shortcut="g")
    def copy_cell(self):
        self.anim.copy_cell(self.nav.cursor)
        self.move_cell_forward()

    @op.operation(name="Cloner l'image", shortcut="h")
    def clone_cell(self):
        self.anim.clone_cell(self.nav.cursor)
        self.nav.next_cell()

    @op.operation(name="Suprimer l'image", shortcut="c")
    def del_cell(self):
        self.anim.del_cell(self.nav.cursor)
        self.nav.prev_cell()

    @op.operation(name="Effacer l'image", shortcut="v")
    def clear_cell(self):
        self.nav.current_cell().clear()
