# -*-coding:Utf-8 -*

"""
Ce module est pour le tableau de commande

"""
import tkinter as tk
import os
import re
# from tkinter.ttk import *


class ButtonTable(tk.Frame):
    """Un ButtonTable  est une Frame avec des ButtonTable.Button"""

    def __init__(self, parent):
        super().__init__(parent)

    def add_button(self, img, command):
        return ButtonTable.Button(self, img=img, command=lambda e: command())

    class Button(tk.Label):
        """Un ButtonTable.Button est un petit bouton"""
        # on pourra acceder aux icones grace à ButtonTable.Button.icns["nom.xbm"]
        icns = {}

        def change_icn(self, img):
                """cette method permet de changer l'icn d'un bouton"""
                # si le bouton existe on le met, sinon on met none.xbm
                icns = ButtonTable.Button.icns
                img_name = img + ".xbm"
                icon = icns[img_name] if img_name in icns else icns["none.xbm"]
                self.config(image=icon)

        def __init__(self, master, img="none", command=None, id=0):
            """ id est utile pour les cell button, img doit etre le nom de l'icone sans l'extension, command est la fonction qui est appellée quand on clic sur le bouton"""
            super().__init__(master)

            # si Button.icns n'est pas encore plein d'icones, on le rempli avec tout ce qu'on trouve
            icns = ButtonTable.Button.icns
            if len(icns) == 0:
                for f in os.listdir("resources/icns"):
                    if re.search(r'.+\.xbm', f):
                        icns[f] = tk.BitmapImage(file="resources/icns/"+f)

            self.id = id
            self.change_icn(img)
            self.bind("<Button 1>", command)
            self.pack(side=tk.LEFT)
