"""This module provide control functions to manage projects"""

from .. import projects
from . import change_project_state
from . import change_cursor_state

class ProjectNotFoundError(FileNotFoundError):
    """This error is raised when project to be loaded is not found."""
    pass

@change_cursor_state
def load(cursor, name=None):
    """
    Just call the projects.load function so it load project from default directory.
    """
    name = name or cursor.proj.name
    try:
        cursor.proj = projects.load(name)
    except FileNotFoundError:
        raise ProjectNotFoundError()    


@change_cursor_state
def get(cursor, name=None):
    """
    Just call the projects.get function so it first try to get an already loaded
    project, then to load project from default directory, then to create it.
    """
    name = name or cursor.proj.name
    cursor.proj = projects.get(name)


@change_project_state
def save(cursor, name=None):
    """
    Just call the projects.save function so it write datas in the default dir.
    """
    cursor.proj.name = name or cursor.proj.name
    projects.save(cursor.proj)
