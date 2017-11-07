# -*-coding:Utf-8 -*
from interface import board
from control import pencil


class DrawingBoard(board.Board):
    """C'est là où on dessine
    C'est un objet qui hérite de Board"""

    def __init__(self, parent):
        """Constructeur du board.
        on y innitialise les variables et evenements qui servent au dessin"""
        super().__init__(parent)
        # Le crayon
        self.pencil = pencil.Pencil()
        # Les evenements qui font le dessin
        self.canvas.bind('<Button 1>', self._start_drawing)
        self.canvas.bind('<ButtonRelease 1>', self._stop_drawing)
        self.canvas.bind('<Motion>', self._keep_drawing)
        self.canvas.bind_all('<BackSpace>', self._erase)
        # Boléens qui disent si on est en train de dessiner
        self.is_drawing = False
        # Là où on stock les coordonées de la ligne que l'on dessine
        self.line_coords = []

    def _start_drawing(self, event):
        """Cette fonction commence le trait"""
        # On commence la ligne
        self.line_coords = [event.x, event.y]
        # On annonce que le dessin est en cours
        self.is_drawing = True

    def _stop_drawing(self, event):
        """Cette fonction termine le trait"""
        # On envoie les infos au pencil
        self.pencil.save_line()
        # On annonce que le dessin est fini
        self.is_drawing = False

    def _keep_drawing(self, event):
        """Cette fonction dessine le trait"""
        if self.is_drawing:
            # On garde en mémoire les coordonnées du point
            self.line_coords.append(event.x)
            self.line_coords.append(event.y)
            # On envoie les infos au pencil
            self.pencil.draw_tmp_line(self.line_coords, self.nav[0].current_cell())
            self.reset()

    # ERASE = PB ENCORE A REGLER !!!
    # AUSSI : PB DE RESET

    def _erase(self, event):
        """Cette fonction efface un trait"""
        if not self.is_drawing:
            # on récupere l'id de l'ellement sous la souris
            current_list = self.canvas.find_withtag(CURRENT)
            if current_list:
                id_to_del = current_list[0]
                if len(self.canvas.gettags(id_to_del)) > 1:
                    # on récupère les tags de cet element -> ["l4", "current"] (par exemple, pour la 4ème ligne)
                    # on prend le premier tag -> "l4"
                    # on enlève le premier caractère -> "4"
                    # on transforme en int -> 4
                    line_to_del = int(self.canvas.gettags(id_to_del)[0][1:])
                    # on suprime la ligne directement dans la liste lines de la current_cell
                    del self.nav.current_cell().lines[line_to_del]
                    # on reset
                    self.reset()
