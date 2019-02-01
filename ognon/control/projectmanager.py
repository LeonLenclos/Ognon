"""This module provide control functions to manage projects"""
import os, pickle, shutil, configparser

from .. import model
from .. import view

def load(cursor, name=None):
    """Load from files. If files does not exist, create they"""
    name = name or cursor.proj.name
    cursor.proj = model.Project(name)
    if not os.path.isdir(view.get_path(cursor)):
        os.mkdir(view.get_path(cursor))
        os.mkdir(view.get_path(cursor, 'export'))
        shutil.copy('ognon/config.ini', view.get_path(cursor))
        save(cursor)

    # Load anims (*.ogn)
    cursor.proj.anims = {}
    for file in os.listdir(view.get_path(cursor)):
        if file.endswith('.ogn'):
            with open(view.get_path(cursor, file), 'rb') as fi:
                cursor.proj.anims[file[:-4]] = pickle.load(fi)
    # Load config (config.ini)
    config = configparser.ConfigParser()
    config.read('ognon/config.ini')
    cursor.proj.config = {k:dict(v) for k, v in dict(config).items()}


def save(cursor):
    """Save to files."""
    # Save anims (*.ogn)
    for name, anim in cursor.proj.anims.items():
        with open(view.get_path(cursor, name + '.ogn'), 'wb') as fi:
            pickle.dump(anim, fi)

