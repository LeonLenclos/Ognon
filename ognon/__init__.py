"""
Ognon is a a local-only web application for the creation of 2D animation.
Run `python -m ognon` to start the server. Then browse http://lacalhost:40460
"""
import os

__version__ = '1.α'
DEFAULT_HTTP_ADRESS = ('localhost', 40460)
DEFAULT_OSC_ADRESS = ('localhost', 50460)
PROJECTS_DIR = os.path.expanduser('~/ognons/')


from . import model
from . import control
from . import server
from . import view
from . import cursor
from . import projects
from . import tags
from . import utils
