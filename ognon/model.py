"""
This module define the Ognon model

It describes every data that can be write on the disk. they are nested python
classes. With no method description.
"""

        

class Element():
    """
    This class is the super class for all elements.

    An element is an object that can be placed into a layer's elements list
    """
    pass

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
    def __init__(self, lines=None):
        """Init a Cell"""
        self.lines = lines or []

class AnimRef(Element):
    """
    This class describe AnimRefs.

    An animref is a reference to another animation in the same project. It allow
    to include animations in other animations. It has a name attribute, the name
    of the animation it referes to.
    """
    def __init__(self, name):
        """Init an AnimRef with its name"""
        self.name = name

class Layer():
    """
    This class describe Layers.

    A layer contain Elements in an 'elements' list.
    """
    def __init__(self, elements=None):
        """Init a Layer with a first Cell"""
        self.elements = elements or [Cell()]

class Anim():
    """
    This class describe Anims.

    An anim contain Layers in a 'layers' list.
    """
    def __init__(self, layers=None):
        """Init an Anim with a first Layer"""
        self.layers = layers or [Layer()]


# get default config
import configparser
parser = configparser.ConfigParser()
parser.read('ognon/default.ini')
default_config = {k:dict(v) for k, v in dict(parser).items()}

class Project():
    """
    This class describe Projects.

    A project contain Anims in an 'anims' dict where keys are anims names.
    A Project also has a name and a config dict. 
    """

    def __init__(self, name, anims=None, config=None):
        """
        Init an Project with its name.
        
        a dict of anims and a dict of config can also be passed.
        default for anims is a dict containing a single Anim named 'master'.
        default for config is default.ini content
        """
        self.name = name
        self.anims = anims or {'master':Anim()}
         

        self.config = config or default_config