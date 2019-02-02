"""
Ognon is a a local-only web application for the creation of 2D animation.
Run `python -m ognon` to start the server. Then browse http://lacalhost:40460
"""
import os

__version__ = '1.α'
DEFAULT_ADRESS = ('localhost', 40460)
WORKING_DIR = os.path.expanduser('~/ognons/')

from . import model
from . import control
from . import server
from . import view
from . import cursor
