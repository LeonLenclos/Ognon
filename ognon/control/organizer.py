from model import Cell, Layer

class Organizer():
    def __init__(self, ognproject):
        self.ognproject = ognproject

    def add_ognobject_at(self, cursor, ognobject, i):
        if cursor.get_layer() is not None:
            cursor.get_layer().frms.insert(i, ognobject)

    def add_ognobject_after(self, cursor, ognobject):
        if cursor.get_frm_idx() is not None:
            self.add_ognobject_at(cursor, ognobject, cursor.get_frm_idx())

    def add_ognobject_before(self, cursor, ognobject):
        if cursor.get_frm_idx() is not None:
            self.add_ognobject_at(cursor, ognobject, cursor.get_frm_idx()-1)

    def add_cell_after(self, cursor):
        self.add_ognobject_after(cursor, Cell())

    def add_cell_before(self, cursor):
        self.add_ognobject_before(cursor, Cell())

    def add_anim_after(self, cursor, name):
        self.add_ognobject_after(cursor, self.ognobject.anims[name])

    def add_anim_before(self, cursor, name):
        self.add_ognobject_before(cursor, self.ognobject.anims[name])

    def pop_ognobject_at(self, cursor, i):
        if cursor.get_layer() is not None:
            return cursor.get_layer().frms.pop(i)

    def pop_ognobject(self, cursor):
        if cursor.get_frm_idx() is not None:
            return self.pop_ognobject_at(cursor, cursor.get_frm_idx())

    def move_ognobject_from_to(self, cursor, idx, dest):
        ognobject = self.pop_ognobject_at(cursor, idx)
        self.add_ognobject_at(cursor, ognobject, dest)

    def move_ognobject_forward(self, cursor):
        if cursor.get_frm_idx() is not None:
            self.move_ognobject_from_to(cursor, cursor.get_frm_idx(), cursor.get_frm_idx())

    def move_ognobject_backward(self, cursor):
        if cursor.get_frm_idx() is not None:
            self.move_ognobject_from_to(cursor, cursor.get_frm_idx(), cursor.get_frm_idx()-1)

    def copy_ognobject(self, cursor):
        if cursor.get_frm() is not None:
            self.add_ognobject_after(cursor, cursor.get_frm().copy())

    def clone_cell(self, cursor):
        if cursor.get_frm() is not None:
            self.add_ognobject_after(cursor, cursor.get_frm())

    def add_layer(self, cursor):
        if cursor.get_anim() is not None :
            idx = cursor.get_layer_idx() or 0
            cursor.get_anim().layers.insert(idx, Layer())
