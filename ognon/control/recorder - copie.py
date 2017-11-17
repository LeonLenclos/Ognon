import PIL.Image
import PIL.ImageDraw
import pickle
import os

from settings import *
from control import operation as op
from model import animation


class Recorder():
    """docstring for Navigator"""
    def __init__(self, parent):
        self.parent = parent
        self.anim = parent.animation
        self.navig = parent.navigator

    def save_cell(self, cell, path):
        """sauve une image cell dans un fichier path"""
        # on cree une image PIL
        img = PIL.Image.new("RGB", (self.anim.width * settings['export scale'], self.anim.height * settings['export scale']), 'white')
        draw = PIL.ImageDraw.Draw(img)
        # on redessine chaque ligne
        for line in cell.lines:
            line_scaled = [coord * settings['export scale'] for coord in line]
            draw.line(line_scaled, 'black', width=settings["pen width"] * settings['export scale'])
        # on la sauve
        img.save(path)

    ##############
    # OPERATIONS #
    ##############

    @op.operation('directory', name="Sauver les images", shortcut="z")
    def save_all_cells(self, directory):
        """enregistre chaque cell dans un png"""
        i = 0
        for cell in self.anim:
            self.save_cell(cell, directory + str(i).zfill(4) + ".png")
            i += 1

    @op.operation('save_file_png', name="Sauver l'image", shortcut="x")
    def save_curent_cell(self, file_path):
        """enregistre la current_cell dans un png"""
        self.save_cell(self.navig.current_cell(), file_path)

    @op.operation('save_file_ogn', name="Sauver le projet", shortcut="c")
    def save_ognon(self, file_path):
        """enregistre le projet dans un .ogn"""
        with open(file_path, 'wb') as fi:
            pickler = pickle.Pickler(fi)
            pickler.dump(self.anim)

    @op.operation('open_file_ogn', name="Ouvrir le projet", shortcut='v')
    def open_ognon(self, file_path):
        """charge un projet enregistré"""
        with open(file_path, 'rb') as fi:
            un_pickler = pickle.Unpickler(fi)
            anim = un_pickler.load()
            #on load l'anim
            self.parent.load(anim)

    @op.operation(("int", "Largeur", 1920), ("int", "Hauteur", 1080), ("str", "Titre", 'sans titre'), name="Nouveau projet", shortcut='b')
    def new_ognon(self, w, h, title):
        """cré un nouveau projet"""
        self.parent.load(animation.Animation(w, h, title))

    @op.operation('directory', name="Convertir fichiers ogn en png", shortcut='n')
    def ognons_to_png(self, directory):
        """charge un projet enregistré"""
        os.mkdir(directory + "export/")
        print("START EXPORTING...")
        for fi_name in os.listdir(directory):
            if fi_name.endswith(".ogn"):
                fi_path = '{}{}'.format(directory, fi_name)
                with open(fi_path, 'rb') as fi:
                    un_pickler = pickle.Unpickler(fi)
                    self.anim = un_pickler.load()
                    #on load l'anim
                    os.mkdir('{0}export/{1}/'.format(directory, fi_name[:-4]))
                    self.save_all_cells('{0}export/{1}/{1}'.format(directory, fi_name[:-4]))
                    print(".", end='')
        self.anim = self.parent.animation
        print("EXPORTING GOES WELL AND IT IS DONE")
