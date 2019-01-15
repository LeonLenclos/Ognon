#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
Ognon2 is a a software application for the creation of 2D animation
This module describe the OgnProject()
"""
import sys
import os
import configparser
import pickle

import control
import model

class OgnProject():
    """An OgnProject"""

    default_config = configparser.ConfigParser()
    working_dir = ""

    def __init__(self, name):
        """Init an ognon project. name is a string and can be path-like.
        If the project does not exists as a dir in the working_dir, create it. """
        self.name = name
        self.anims = {}
        self.config = configparser.ConfigParser()

        if not self.load():
            print('create')
            self.create()

        self.cursors = []
        self.new_cursor()
        
        self.controllers = {
            "animsmanager": control.AnimsManager(self),
            "navigator": control.Navigator(self),
            "render":    control.Render(self),
            "organizer": control.Organizer(self),
            "drawer":    control.Drawer(self),
        }

    def get_path(self, file=""):
        """Return path to the project (or path to a file in the project)."""
        return os.path.join(self.working_dir, self.name, file)

    def load(self):
        """Load from files. If files exists return True, else, return False"""
        if not os.path.isdir(self.get_path()):
            return False
        # Load anims (*.ogn)
        self.anims = {}
        for file in os.listdir(self.get_path()):
            if file.endswith('.ogn'):
                with open(self.get_path(file), 'rb') as fi:
                    self.anims[file[:-4]] = pickle.load(fi)
        # Load config (config.ini)
        self.config.clear()
        self.config.read(self.get_path('config.ini'))
        return True
    
    def create(self):
        """Create the project"""
        os.mkdir(self.get_path())
        self.anims['master'] =  model.Anim()
        self.save()

    def save(self):
        """Save to files."""
        # Save anims (*.ogn)
        for name, anim in self.anims.items():
            with open(self.get_path(name + '.ogn'), 'wb') as fi:
                pickle.dump(anim, fi)
        # Save config (config.ini)
        with open(self.get_path('config.ini'), 'w') as configfile:
            self.config.write(configfile)

    def ask(self, request):
        """Process a request. The request must have a "method" key with the
        method to be called. Other keys are passed to the method as kwargs."""
        cursor_idx = request.pop('cursor_idx')
        cursor = self.cursors[cursor_idx]
        
        
        if 'method' in request:
            if request["method"] == "control":
                request['cursor'] = cursor
            elif request["method"] == "del_cursor":
                request['i'] = cursor_idx
            method = getattr(self, request.pop("method"))
            method(**request)

        return {
            'lines':self.controllers['render'].get_lines(cursor),
            'anims':list(self.anims.keys()),
            'cursors':len(self.cursors),
            'cursor':{
                'anim_name':cursor.get_anim_name(),
                'layer_idx':cursor.get_layer_idx(),
                'frm_idx':cursor.get_frm_idx(),
                'playing':cursor.playing,
            },
            'timeline':{
                'len':len(cursor.get_anim()),
                'elmnts':[[{
                            'type':str(frm),
                            'len':len(frm),
                        } for frm in layer.frms
                    ] for layer in cursor.get_anim().layers
                ],
            } if cursor.get_anim() else {'len':0,'elmnts':[]},
            'config':self.get_config_dict()
        }

    def control(self, controller, controller_method, **kwargs):
        """Call the controller_method method of the controller."""
        method = getattr(self.controllers[controller], controller_method)
        method(**kwargs)

    def new_cursor(self):
        """Add a new Cursor to cursors list."""
        self.cursors.append(control.Cursor(self))

    def del_cursor(self, i=0):
        """Delete a Cursor from cursors list."""
        del self.cursors[i]

    def get_config(self, section, option, convert_type=None):
        """Get the value of the given option. First check in config then in
        default_config"""
        convert = lambda o: o
        if convert_type is int:
            convert = lambda o: int(o)
        elif convert_type is bool:
            convert = lambda o: o == 'true'

        try:
            return convert(self.config[section][option])
        except KeyError:
            return convert(self.default_config[section][option])

    def get_config_dict(self):
        """Get the config dict"""
        d = {}
        for key, section in self.default_config.items():
            d[key] = {}
            for option, value in section.items():
                d[key][option] = self.get_config(key, option)
        return d

    def set_config(self, section, option, value):
        """Set the value of the given option"""
        self.config.set(section, option, value)

OgnProject.default_config.read('config.ini')
OgnProject.working_dir = os.path.expanduser(
    OgnProject.default_config['project']['working_dir'])
os.makedirs(OgnProject.working_dir, exist_ok=True)