import tkinter as tk

from interface import board, table
from control import navigator, organizer


class AnimationWindow(tk.Toplevel):
    """Fenetre d'animation"""
    def __init__(self):
        super().__init__()

        # Taille et titre de la fenêtre
        self.title("Animation")
        self.geometry("{}x{}".format(300, 300))

        self.bind("<Button-1>", lambda e: self.focus_set())


        #innitialisation des machines
        self.animation = None
        self.navigator = None
        self.organizer = None


    def load(self, anim):
        """permet de charger une nouvelle anim"""
        #on supprime tous les widget
        for child in self.winfo_children():
            child.destroy()

        #on reinitialise les machines
        self.animation = anim
        self.navigator = navigator.Navigator(self.animation)
        self.organizer = organizer.Organizer(self.navigator)

        # on cree un board
        self.board = board.DrawingBoard(self)
        self.board.add_navigator(self.navigator)
        self.board.pack(fill="both", expand=1)

        # on cree la timeline
        self.time_line = table.TimeLine(self, self.navigator)
        self.time_line.pack(side=tk.BOTTOM)

        # on cree les tables
        self.organizer_table = table.OperationTable(self, self.organizer).pack(side=tk.BOTTOM)
        self.navigator_table = table.OperationTable(self, self.navigator).pack(side=tk.BOTTOM)

class BoardWindow(tk.Toplevel):
    """Fenetre d'animation"""
    def __init__(self):
        super().__init__()

        # Taille et titre de la fenêtre
        self.title("Board")
        self.geometry("{}x{}".format(300, 300))

        self.board = board.Board(self)
        self.board.pack(fill="both", expand=1)
        self.board.show_onion = False
        self.state = False
        self.bind_all("<F11>", self.toggle_fullscreen)
        self.bind_all("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.attributes("-fullscreen", self.state)
        print("toggle fullscreen")
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"
    def add_navigator(self, nav):
        """permet de charger une nouvelle anim"""
        self.board.add_navigator(nav)


class ClockWindow(tk.Toplevel):
    """Fenetre d'horloge"""
    def __init__(self):
        super().__init__()

        # Taille et titre de la fenêtre
        self.title("Clock")
        self.geometry("{}x{}".format(80, 25))
        self.clock = table.Clock(self)
        self.clock.pack()

    def add_navigator(self, nav):
        """permet de charger une nouvelle anim"""
        self.clock.add_navigator(nav)
