from interface import button_table as bt


class TimeLine(bt.ButtonTable):
    """Une TimeLine est un CommandBoard un peu spécial"""

    def __init__(self, parent, nav):
        super().__init__(parent)

        self.nav = nav
        nav.add_listener(self.reset)

        # Rangement boutons cell
        self.cells_buttons = []
        self.specials_cells_buttons = []

        # On reset une première fois
        self.reset()

    def reset(self):
        # On détruits tous les cells buttons
        for button in self.cells_buttons:
            button.destroy()
        self.cells_buttons = []
        self.specials_cells_buttons = []

        # On recrée un bouton par cell
        i = 0
        for cell in self.nav.anim:
            # on cherche les boutons speciaux pour les avoir sous la main lors de soft_reset si c'en est un track_it vaudra True a la fin
            track_it = True
            # on construit l'icone qu'il faut
            icone = 'cell'
            if i == self.nav.cursor:
                if cell.occurrences > 1:
                    icone += "_clone"
                icone += "_select"
            elif cell is self.nav.current_cell():
                icone += "_clone"
            else:
                track_it = False  # rien de spécial

            # on cree un  bouton
            command = lambda e: self.nav.go_to_cell(e.widget.id)
            new_button = bt.ButtonTable.Button(self, img=icone, command=command, id=i)

            # on le range dans cells_buttons
            self.cells_buttons.append(new_button)
            # on le ranfe dans specials_cells s'il faut
            if track_it:
                self.specials_cells_buttons.append(new_button)

            i += 1

    # PAS ENCORE REVU A PARTIR DE LÀ !!!!!

    def soft_reset(self):
        #l'idée du soft reset est de ne pas etre trop lourd pour quand on en a pas besoin
        # donc au lieu de tout supprimer et de tout recreer comme dans le reset(),
        # on va juste changer les trucs qui ont changé

        #on ne fait ça que si la taille de l'anim n'a pas changé
        if len(self.anim) == len(self.cells_buttons):
            # on commence par donner une apparence normale à tous les boutons spéciaux
            for button in self.specials_cells_buttons:
                button.change_icn('cell')
            # on réinitialise la liste des boutons speciaux avec comme premier ellement le bouton de la current_cell
            self.specials_cells_buttons = []
            self.specials_cells_buttons.append(self.cells_buttons[self.nav.cursor])
            # si cette cell n'as pas de clone on lui donne l'apparence d'une cell_select
            if self.nav.current_cell().occurrences == 1:
                self.cells_buttons[self.nav.cursor].change_icn('cell_select')
            #si elle a des clones alors on lui donne l'apparence qu'il faut
            # et on va chercher tous ses clones pour leur donner l'apparence qu'il faut et les ranger dans les boutons speciaux
            else:
                self.cells_buttons[self.nav.cursor].change_icn('cell_clone_select')
                i = 0
                for cell in self.anim:
                    if cell is self.nav.current_cell() and not self.nav.cursor == i:
                        self.cells_buttons[i].change_icn('cell_clone')
                        self.specials_cells_buttons.append(self.cells_buttons[i])
                    i += 1
