import PIL.Image
import PIL.ImageDraw
import pickle
import os
import io

from control import operation as op
from model import animation


class Recorder():
    """docstring for Navigator"""
    def __init__(self, path="/"):
        self.path = path
        #pref
        self.bg_color = 'white'
        self.stroke_color = 'black'
        self.stroke_weight = 2
        self.image_format = 'png'
        self.scale = 1

    def save(self, bytes, file_name):
        path = self.path + file_name
        with open(path, 'wb') as f:
            f.write(bytes.getvalue())

    def open(self, file_name):
        path = self.path + file_name
        with open(path, 'rb') as f:
            return f

    def cell_to_img(self, cell):
        # on cree une image PIL
        w = cell.parent.width * self.scale
        h = cell.parent.height * self.scale
        img = PIL.Image.new("RGB", (w, h), self.bg_color)
        # on redessine chaque ligne
        draw = PIL.ImageDraw.Draw(img)
        for l in cell.lines:
            scaled = [coord * self.scale for coord in l]
            w = self.stroke_weight * self.scale
            draw.line(scaled, self.stroke_color, width=w)
        # on retourne l'image
        output = io.BytesIO()
        img.save(output, format=self.image_format)
        return output

    def animation_to_ogn(self, anim):
        output = io.BytesIO()
        pickler = pickle.Pickler(output)
        pickler.dump(self.anim)
        return output

    def ogn_to_animation(self, file):
        unpickler = pickle.Unpickler(fi)
        anim = unpickler.load()
        return anim

    def save_cell(self, cell):
        """sauve une image cell dans un fichier path"""
        file_name = "%s-cell%04d.%s" % (cell.parent.title, cell.id, self.format)
        img = self.cell_to_img(cell)
        self.save(img, file_name)

    def save_all_cells(self, anim):
        i = 0
        for c in anim:
            file_name = "%s/%04d.%s" % (anim.title, i, self.format)
            img = self.cell_to_img(c)
            self.save(img, file_name)
            i += 1

    def new_animation(self, width=1920, height=1080, title="sans-titre"):
        anim = animation.Animation(width, height, title)
        return anim

    def rename_animation(self, animation, title):
        anim.title = str(title)

    def save_animation(self, anim, title=None):
        if as_title is not None:
            self.rename_animation(anim, title)
        file_name = "%s.%s" % (anim.title, 'ogn')
        ogn = self.animation_to_ogn(anim)
        self.save(ogn, file_name)

    def open_animation(self, title):
        ogn = self.open(title + ".ogn")
        anim = self.ogn_to_animation(ogn)
        return anim


    ##############
    # OPERATIONS #
    ##############

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
