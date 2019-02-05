"""
This module is the project loader. His role is to load projects from files and
also to keep in memory all loaded projects by names to provide preloaded
projects.
"""
import os, pickle, shutil, configparser, pathlib

from . import model
from . import PROJECTS_DIR

projects = {}

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
    parser = configparser.ConfigParser()
    parser.read(os.path.join(path, 'config.ini'))
    config = {k:dict(v) for k, v in dict(parser).items()}
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
    # save anims
    for name, anim in project.anims.items():
        with open(os.path.join(path, name+'.ogn'), 'wb') as fi:
            pickle.dump(anim, fi)
    # save config
    parser = configparser.ConfigParser()
    parser.read_dict(project.config)
    with open(os.path.join(path, 'config.ini'), 'w') as fi:
        parser.write(fi)

def save(project):
    """
    Save the project in the projects directory
    """
    save_project_at(project, PROJECTS_DIR + project.name)
