"""
This module is the project loader. His role is to load projects from files and
also to keep in memory all loaded projects by names to provide preloaded
projects.
"""

import os
import pickle
import shutil
import configparser
import pathlib

from . import model
from . import PROJECTS_DIR
from . import utils

projects = {}

def get_saved_projects_list():
    """
    Return a list of all of saved projects name.

    Return a list of dirs in the projects directory. ignore dirs starting with a
    dot or an underscore.
    """
    ignore_files = lambda d: d[0] not in ('.', '_')
    return list(filter(ignore_files, os.listdir(PROJECTS_DIR)))

def load_from_path(path):
    """
    Load the ognon project at the specified path. store it in the projects dict
    and return it.
    """
    # Get name from path
    name = pathlib.Path(path).parts[-1]
    # Load anims
    anims = {}
    for file in os.listdir(path):
        if file.endswith('.ogn'):
            with open(os.path.join(path, file), 'rb') as fi:
                anims[file[:-4]] = pickle.load(fi)
    # Load config
    try:
        config = utils.parse_config(os.path.join(path, 'config.ini'))
    except FileNotFoundError:
        config = utils.parse_config(utils.pkgabspath('default.ini'))
    # Create, store and return project
    project = model.Project(name, anims=anims, config=config)
    projects[name] = project
    return project

def load(name):
    """
    Load the project in the default projects directory, store it in the projects
    dict and return it.
    """
    return load_from_path(PROJECTS_DIR + name)

def new(name):
    """
    Create a new project, store it in the projects dict and return it.
    """
    project = model.Project(name)
    projects[name] = project
    return project

def get(name):
    """
    return a project from the project dict. If the project does not exist,
    load it from the projects directory, if it does not exists there neither,
    create it.
    """
    try:
        return projects[name]
    except KeyError:
        try:
            return load(name)
        except FileNotFoundError:
            return new(name)

def save_project_at(project, path):
    """
    Save the project object at the given path. 
    """
    # create dir
    if not os.path.isdir(path):
        os.mkdir(path)
        os.mkdir(os.path.join(path, 'export'))
        shutil.copyfile(utils.pkgabspath('default.ini'), os.path.join(path, 'config.ini'))
    # save anims
    for name, anim in project.anims.items():
        with open(os.path.join(path, name+'.ogn'), 'wb') as fi:
            pickle.dump(anim, fi)
    # # dont save config
    # parser = configparser.ConfigParser()
    # parser.read_dict(project.config)
    # with open(os.path.join(path, 'config.ini'), 'w') as fi:
    #     parser.write(fi)

def save(project):
    """
    Save the project in the projects directory
    """
    save_project_at(project, PROJECTS_DIR + project.name)

def close(name):
    """
    Remove project from projects dict.
    """
    del projects[name]

def delete(name):
    """
    Delete project from disk.
    """
    shutil.rmtree(PROJECTS_DIR + name)
