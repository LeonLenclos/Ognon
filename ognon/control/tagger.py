"""This module provide control functions to tags elements"""

def add_tag(cursor, tag):
    """Add a tag to the element"""
    cursor.get_element().tags.append(tag)

def replace_tag(cursor, tag, i):
    """Add a tag to the element"""
    cursor.get_element().tags[i] = tag

def rm_tag(cursor, i):
    """Remove a tag to the element"""
    del cursor.get_element().tags[i]

def rm_tags(cursor):
    """Remove a tag to the element"""
    cursor.get_element().tags = []