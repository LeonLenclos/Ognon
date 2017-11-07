class Cell():
    """Cette class est pour les Cell (frames)
    c'est à dire chaque image de l'animation"""
    def __init__(self, id):
        """Le constructeur de Cell (recoit un id)"""
        # cette liste contient les coordonnees des lignes
        # sous la forme [[x1,y1,x2,y2,x3,y3...],[],[]...]
        self.lines = []
        # l'id est aussi l'index ou on peut trouver la cell dans la liste cells d'animation
        self.id = id
        self.occurrences = 1

    def add_line(self, coords):
        """cette fonction ajoute une nouvelle ligne à la Cell"""
        self.lines.append(coords)

    def clear(self):
        """cette fonction efface toute les lignes de la Cell"""
        self.lines = []

    def copy(self, id):
        """cette fonction renvoie une copie de l'objet"""
        new_cell = Cell(id)
        for l in self.lines:
            new_cell.add_line(l)
        return new_cell
