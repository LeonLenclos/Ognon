"""
Ognon is a local-only web application for the creation of 2D animation.
Run `python -m ognon` to start the server. Then browse http://localhost:40460
"""
import os

__version__ = '1.α'
HTTP_ADDRESS = ('localhost', 40460)
OSC_ADDRESS = ('localhost', 50460)
PROJECTS_DIR = os.path.expanduser('~/ognons/')

from . import model
from . import server
from . import view
from . import clients
from . import cursor
from . import projects
from . import tags
from . import utils
from . import control
