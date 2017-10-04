# -*-coding:Utf-8 -*

from tkinter import *


class Prompt(Toplevel):
    """cette classe permet de creer une popup qui demande une info a l'uttilisateur"""
    def __init__(self, parent, questions, title=None):

        super().__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
