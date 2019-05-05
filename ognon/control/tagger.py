"""This module provide control functions to tags elements"""
from . import change_project_state

@change_project_state
def add_tag(cursor, tag):
    """Add a tag to the element"""
    cursor.get_element().tags.append(tag)

@change_project_state
def replace_tag(cursor, tag, i):
    """Add a tag to the element"""
    cursor.get_element().tags[i] = tag

@change_project_state
def rm_tag(cursor, i):
    """Remove a tag to the element"""
    del cursor.get_element().tags[i]

@change_project_state
def rm_tags(cursor):
    """Remove a tag to the element"""
    cursor.get_element().tags = []