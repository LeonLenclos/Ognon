"""Ce module est pour la gestion de l'animation.
Un objet Animation
Un objet Frm
"""


class Animation():
    """Cette classe est pour l'animation c'est à dire l'ensemble des frm.
    Elle permet de gérer un ordre pour les frm (self.film) independant de celui de leur creation (self.frms)
    elle permet de supprimer, ajouter, copier, cloner, déplacer des frm
    """

    def __init__(self, w, h, title="sans-titre"):
        """Le constructeur de Animation
        on cree une animation avec une frm"""
        self.width = w
        self.height = h
        self.title = title
        #une liste avec des frms
        self._frms = []
        #une liste avec les id des frms dans l'ordre
        self._film = []
        #une premiere frm
        self.add_frm(0)

    def __len__(self):
        """Renvoie len(self)
        La longueur du film"""
        return len(self._film)

    def __getitem__(self, i):
        """Renvoie self[i]
        l'objet frm correspondant a la position i dans le film"""
        return self._frms[self._film[i]]

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

    def add_frm(self, index):
        """Ajoute une frm à l'animation"""
        # On cree une frm
        frm = Frm(len(self._frms))
        # On la range a la fin de frms et là oû on veut dans film
        self._frms.append(frm)
        self._film.insert(index, frm.id)

    def clone_frm(self, index):
        """Ajoute une frm à l'animation"""
        # On clone une frm
        frm = self[index]
        frm.occurrences += 1
        # On la range juste avant l'originale dans film
        self._film.insert(index, frm.id)

    def copy_frm(self, index):
        """Ajoute une frm à l'animation"""
        # On cree une frm
        frm = self[index].copy(len(self._frms))
        # On la range a la fin de frms et juste avant l'originale dans film
        self._frms.append(frm)
        self._film.insert(index, frm.id)

    def move_frm_to(self, from_i, to_i):
        """Ajoute une frm à l'animation"""
        # On pop une frm dans film située à from_i
        frm = self._film.pop(from_i)
        # On la range dans film à to i
        self._film.insert(to_i, frm)

    def del_frm(self, index):
        """Supprime une frm à l'animation"""
        #on la suprime la frm. si c'est la seule on l'efface
        if len(self._film) == 1:
            self._frms[0].clear()
        else:
            self[index].occurrences -= 1
            del self._film[index]


class Frm():
    """Cette class est pour les Frm (frames)
    c'est à dire chaque image de l'animation"""
    def __init__(self, id):
        """Le constructeur de Frm (recoit un id)"""
        # cette liste contient les coordonnees des lignes
        # sous la forme [[x1,y1,x2,y2,x3,y3...],[],[]...]
        self.lines = []
        # l'id est aussi l'index ou on peut trouver la frm dans la liste frms d'animation
        self.id = id
        self.occurrences = 1

    def add_line(self, coords):
        """cette fonction ajoute une nouvelle ligne à la Frm"""
        self.lines.append(coords)

    def clear(self):
        """cette fonction efface toute les lignes de la Frm"""
        self.lines = []

    def copy(self, id):
        """cette fonction renvoie une copie de l'objet"""
        new_frm = Frm(id)
        for l in self.lines:
            new_frm.add_line(l)
        return new_frm
