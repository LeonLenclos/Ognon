"""Provide a Reader class to navigate into Animation"""

from model import Anim

class AnimsManager():
    """Allow to navigate into one Animation."""
    def __init__(self, ogn_project):
        self.ogn_project = ogn_project

    def new_anim(self, cursor, name):
        """Add a new Anim to anims dict."""
        if name:
            self.ogn_project.anims[name] = Anim()
        self.select_anim(cursor, name)

    def select_anim(self, cursor, name):
        """Set cursor anim name."""
        if name in self.ogn_project.anims:
            cursor.set_anim_name(name)

    def del_anim(self, cursor, name):
        """Delete an Anim from anims dict."""
        print(name)
        if name in self.ogn_project.anims:
            del self.ogn_project.anims[name]
            

