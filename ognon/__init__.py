import os, pytest

__version__ = '1.α'
DEFAULT_ADRESS = ('localhost', 40460)
WORKING_DIR = os.path.expanduser('~/ognons/')

from . import model
from . import control
from . import server
from . import view
from . import cursor

pytest.main(['-x', 'ognon/tests'])
