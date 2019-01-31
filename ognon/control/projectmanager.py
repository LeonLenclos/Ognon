"""This module provide control functions to manage projects"""
import os, pickle, shutil, configparser
from ..model import Project
from .. import model
from .. import WORKING_DIR

def _get_path(cursor, file=""):
    """Return path to the project (or path to a file in the project)."""
    return os.path.join(WORKING_DIR, cursor.proj.name, file)


def load(cursor, name=None):
    """Load from files. If files does not exist, create they"""
    name = name or cursor.proj.name
    cursor.proj = Project(name)
    if not os.path.isdir(_get_path(cursor)):
        os.mkdir(_get_path(cursor))
        shutil.copy('ognon/config.ini', _get_path(cursor))
        save(cursor)

    # Load anims (*.ogn)
    cursor.proj.anims = {}
    for file in os.listdir(_get_path(cursor)):
        if file.endswith('.ogn'):
            with open(_get_path(cursor, file), 'rb') as fi:
                cursor.proj.anims[file[:-4]] = pickle.load(fi)
    # Load config (config.ini)
    config = configparser.ConfigParser()
    config.read('ognon/config.ini')
    cursor.proj.config = {k:dict(v) for k, v in dict(config).items()}


def save(cursor):
    """Save to files."""
    # Save anims (*.ogn)
    for name, anim in cursor.proj.anims.items():
        with open(_get_path(cursor, name + '.ogn'), 'wb') as fi:
            pickle.dump(anim, fi)

