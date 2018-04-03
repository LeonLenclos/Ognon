# -*-coding:Utf-8 -*

"""
Ce module est pour les tableaux de commande

"""
import tkinter as tk
import os
import re

from pythonosc import dispatcher
from pythonosc import osc_server
import threading

from control import operation as op


class ButtonTable(tk.Frame):
    """Un ButtonTable  est une Frame avec des ButtonTable.Button"""

    def __init__(self, parent):
        super().__init__(parent)
        self.shortcuts_dict = {}

    def add_button(self, img, operation, key=None):
        if key is not None:
            self.shortcuts_dict[key] = operation
            self.master.bind("<KeyPress %s>" % key, self.shortcut)
        return ButtonTable.Button(self, img=img, command=lambda e: operation())



    def shortcut(self, event):
        key = event.keysym
        if key in self.shortcuts_dict:
            self.shortcuts_dict[key]()

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


class OperationTable(ButtonTable):
    """docstring for OperationTable"""
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler

        controler_module = controler.__module__
        operations_dict = op.Operation.dic[controler_module]
        for name in operations_dict:
            operation = operations_dict[name].copy()
            operation.target = self.controler
            self.add_button(name, operation, key=operation.shortcut)


class Clock(ButtonTable):
    """"""
    def __init__(self, parent, nav=None):
        super().__init__(parent)
        # Preferences
        self.ips = 6
        self.nav = []
        self.autoruning = False
        self.after_id = ""
        if nav is not None:
            self.add_navigator(nav)
        self.add_button('run', self.run, key='BackSpace')
        self.add_button('autorun', self.autorun, key='Return')
        self.add_button('reset', self.reset)
        self.autorun()
        self.must_run = False;
        self.must_reset = False;

    def do_what_you_must_do(self):
        if self.must_run:
            self.run()
            self.must_run = False
        elif self.must_reset:
            self.reset()
            self.must_reset = False

    def add_navigator(self, nav):
        self.nav.append(nav)

    def run(self):
        for n in self.nav:
            n.run()

    def autorun(self):
        self.autoruning = not self.autoruning
        if self.autoruning:
            self.start()
        else:
            self.stop()

    def reset(self):
        for n in self.nav:
            n.go_to_first_cell()

    def start(self):
        self.run()
        time_in_ms = int(1000 / self.ips)
        self.after_id = self.after(time_in_ms, self.start)

    def stop(self):
        self.after_cancel(self.after_id)

    def osc_sync(self, ip="192.168.1.2", port=5005):
        """ Synchronise the clock with an osc signal
        """

        def step(arg):
            self.must_run = True
            print(arg)

        def reset(arg):
            self.must_reset = True
            print(arg)

        my_dispatcher = dispatcher.Dispatcher()

        my_dispatcher.map("/step", step)
        my_dispatcher.map("/reset", reset)
        my_dispatcher.map("/debug", print)

        print((ip, port))
        self.server = osc_server.ThreadingOSCUDPServer((ip, port), my_dispatcher)
        print("Serving on %s on port %s" % self.server.server_address)
        # server.serve_forever()
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.start()


class TimeLine(ButtonTable):
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
            new_button = ButtonTable.Button(self, img=icone, command=command, id=i)

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
