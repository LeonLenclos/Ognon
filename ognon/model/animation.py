"""Ce module est pour la definition de la classe Animation"""
from model import cell as cl
from model.touch import touch


class Animation():
    """
    L'objet animation permet d'organiser un ensemble de d'objets cell
    """

    def __init__(self, w, h, title):
        """Le constructeur de Animation
        on cree une animation avec une cell"""
        # Les dimensios de l'animation
        self.width = w
        self.height = h
        # Le titre de l'animation
        self.title = title
        # Une liste avec des cells
        self._cells = []
        # Une liste avec les id des cells dans l'ordre
        self._film = []
        # ecouteurs
        self.listeners = []
        # On cree une première cell
        self.add_cell(0)

    def __repr__(self):
        return "Animation(title=%r, w=%r, h=%r, len=%r)" % (self.title, self.width, self.height, len(self))

    def __getstate__(self):
        state = self.__dict__
        state['listeners'] = []
        return state

    def __len__(self):
        """Renvoie len(self)
        La longueur du film"""
        return len(self._film)

    def __getitem__(self, i):
        """Renvoie self[i]
        l'objet cell correspondant a la position i dans le film"""
        return self._cells[self._film[i]]

    def __delitem__(self, i):
        del self._film[i]

    def __iter__(self):
        """implémente iter(self)"""
        self.iter_index = -1
        return self

    def __next__(self):
        """uttilisé pour l'itteration"""
        if self.iter_index >= len(self) - 1:
            raise StopIteration
        self.iter_index += 1
        return self[self.iter_index]

    @touch
    def add_cell(self, index):
        """Ajoute une cell à l'animation"""
        # On cree une cell
        cell = cl.Cell(len(self._cells), self)
        # On la range a la fin de cells et là oû on veut dans film
        self._cells.append(cell)
        self._film.insert(index, cell.id)

    @touch
    def clone_cell(self, index):
        """Ajoute une cell à l'animation"""
        # On clone une cell
        cell = self[index]
        cell.occurrences += 1
        # On la range juste avant l'originale dans film
        self._film.insert(index, cell.id)

    @touch
    def copy_cell(self, index):
        """Ajoute une cell à l'animation"""
        # On cree une cell
        cell = self[index].copy(len(self._cells))
        # On la range a la fin de cells et juste avant l'originale dans film
        self._cells.append(cell)
        self._film.insert(index, cell.id)

    @touch
    def move_cell_to(self, from_i, to_i):
        """Ajoute une cell à l'animation"""
        # On pop une cell dans film située à from_i
        cell = self._film.pop(from_i)
        # On la range dans film à to i
        self._film.insert(to_i, cell)

    @touch
    def del_cell(self, index):
        """Supprime une cell à l'animation"""
        #on la suprime la cell. si c'est la seule on l'efface
        if len(self) == 1:
            self[0].clear()
        else:
            self[index].occurrences -= 1
            del self[index]
