import PIL.Image
import PIL.ImageDraw

from tkinter import *  # ############
from tkinter import filedialog  # ### ces 2 lignes doivent a terme etre supprimées

from settings import *
from operation import *


class Recorder():
    """docstring for Navigator"""
    def __init__(self, parent):
        self.parent = parent
        self.anim = parent.animation

    ##############
    # OPERATIONS #
    ##############

    @operation(name="Sauver les images", shortcut="Control_E")
    def save_all_frames(self):
        directory = filedialog.askdirectory() + "/"
        i = 0
        for cell in self.anim:
            self.save_frame(cell, directory + str(i).zfill(4) + ".png")
            i += 1

    @operation(name="Sauver l'image", shortcut="Control_Shift_E")
    def save_frame(self, cell, path):
        img = PIL.Image.new("RGB", (self.w, self.h), 'white')
        draw = PIL.ImageDraw.Draw(img)
        for line in cell.lines:
            draw.line(line, 'black')
        img.save(path)
