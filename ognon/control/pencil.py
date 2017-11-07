# -*-coding:Utf-8 -*


class Pencil():
    """C'est ce qui dessine"""

    def __init__(self):
        """Constructeur du crayon"""
        # Là où on stock les coordonées de la ligne que l'on dessine
        self.is_drawing = False

    def draw_tmp_line(self, line, cell):
        if self.is_drawing:
            del cell.lines[-1]
        else:
            self.is_drawing = True
        cell.add_line(line)

    def save_line(self):
        self.is_drawing = False

    # ERASE = PB ENCORE A REGLER !!!

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
