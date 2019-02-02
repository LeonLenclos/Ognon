"""
This module prints information about the Ognon session and start the server.
"""

import pytest

from . import server
from . import __version__, WORKING_DIR, DEFAULT_ADRESS

pytest.main(['-x', 'ognon/tests'])

title = ' Ognon v{} '.format(__version__)
print('+{line}+\n|{title}|\n+{line}+'.format(line='-'*len(title), title=title))
print("Working on file://{}".format(WORKING_DIR))
print("Serving on http://{}:{}".format(*DEFAULT_ADRESS))

server.serve(DEFAULT_ADRESS)