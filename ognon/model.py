"""
This module define the Ognon model

It describes every data that can be write on the disk. they are nested python
classes. With no method description.
"""

from . import utils


class Element():
    """
    This class is the super class for all elements.

    An element is an object that can be placed into a layer's elements list
    """
    def __init__(self, tags=None):
        """Init an Element"""
        self.tags = tags or []


class Line():
    """
    This class describe Lines.

    A line has a list of coords that should look like :
    ::
    
        [x1, y1, x2, y2, x3, y3, ...]
    """
    def __init__(self, coords):
        """Init a Line with the coords list"""
        self.coords = coords
    

class Cell(Element):
    """
    This class describe Cells.

    A cell is the ellement made for draw on it. It has a list of lines.
    """
    def __init__(self, lines=None, tags=None):
        """Init a Cell"""
        super().__init__(tags)
        self.lines = lines or []


class AnimRef(Element):
    """
    This class describe AnimRefs.

    An animref is a reference to another animation in the same project. It allow
    to include animations in other animations. It has a name attribute, the name
    of the animation it referes to.
    """
    def __init__(self, name, tags=None):
        """Init an AnimRef with its name"""
        super().__init__(tags)
        self.name = name

class BrokenElement(Element):
    """
    This class describe a BrokenElement.

    It should not be inside an animation but it's returned by some functions
    if the asked element is broken (e.g. unexisting animref)
    """
    def __init__(self, name, tags=None):
        """Init an BrokenElement with its name"""
        super().__init__(tags)
        self.name = name

class Layer():
    """
    This class describe Layers.

    A layer contain Elements in an 'elements' list.
    """
    def __init__(self, elements=None):
        """Init a Layer with a first Cell"""
        self.elements = elements if elements is not None else [Cell()]


class Anim():
    """
    This class describe Anims.

    An anim contain Layers in a 'layers' list.
    """
    def __init__(self, layers=None):
        """Init an Anim with a first Layer"""
        self.layers = layers if layers is not None else [Layer()]


class Project():
    """
    This class describe Projects.

    A project contain Anims in an 'anims' dict where keys are anims names.
    A Project also has a name, config dict and two states id that should be
    incremented each time the project changes. 'state_id' should be incremented
    when the project organisation changes. 'draw_state_id' should be
    incremented when the content of the elements changes.
    """

    def __init__(self, name, anims=None, config=None):
        """
        Init an Project with its name.
        
        a dict of anims and a dict of config can also be passed.
        default for anims is a dict containing a single Anim named 'master'.
        default for config is default.ini content
        """
        self.name = name
        self.anims = anims if anims is not None else {'master':Anim()}
        self.state_id = 0
        self.draw_state_id = 0

        self.config = config or utils.parse_config(
            utils.pkgabspath('default.ini')
        )
