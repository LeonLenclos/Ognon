import PIL.Image
import PIL.ImageDraw

from settings import *
from operation import *

import pickle
import animation


class Recorder():
    """docstring for Navigator"""
    def __init__(self, parent):
        self.parent = parent
        self.anim = parent.animation
        self.navig = parent.navigator

    def save_cell(self, cell, path):
        """sauve une image cell dans un fichier path"""
        # on cree une image PIL
        img = PIL.Image.new("RGB", (self.anim.width, self.anim.height), 'white')
        draw = PIL.ImageDraw.Draw(img)
        # on redessine chaque ligne
        for line in cell.lines:
            draw.line(line, 'black')
        # on la sauve
        img.save(path)

    ##############
    # OPERATIONS #
    ##############

    @operation('directory', name="Sauver les images", shortcut="z")
    def save_all_cells(self, directory):
        """enregistre chaque cell dans un png"""
        i = 0
        for cell in self.anim:
            self.save_cell(cell, directory + str(i).zfill(4) + ".png")
            i += 1

    @operation('save_file_png', name="Sauver l'image", shortcut="x")
    def save_curent_cell(self, file_path):
        """enregistre la current_cell dans un png"""
        self.save_cell(self.navig.current_cell(), file_path)

    @operation('save_file_ogn', name="Sauver le projet", shortcut="c")
    def save_ognon(self, file_path):
        """enregistre le projet dans un .ogn"""
        with open(file_path, 'wb') as fi:
            pickler = pickle.Pickler(fi)
            pickler.dump(self.anim)

    @operation('open_file_ogn', name="Ouvrir le projet", shortcut='v')
    def open_ognon(self, file_path):
        """charge un projet enregistré"""
        with open(file_path, 'rb') as fi:
            un_pickler = pickle.Unpickler(fi)
            anim = un_pickler.load()
            #on load l'anim
            self.parent.load(anim)

    @operation(("int", "Largeur"), ("int", "Hauteur"), ("str", "Titre"), name="Nouveau projet", shortcut='b')
    def new_ognon(self, w, h, title):
        """cré un nouveau projet"""
        self.parent.load(animation.Animation(w, h, title))
