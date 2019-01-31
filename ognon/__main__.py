from .server import serve
from . import __version__, WORKING_DIR, DEFAULT_ADRESS

title = ' Ognon v{} '.format(__version__)
print('+{line}+\n|{title}|\n+{line}+'.format(line='-'*len(title), title=title))
print("Working on file://{}".format(WORKING_DIR))
print("Serving on http://{}:{}".format(*DEFAULT_ADRESS))

serve(DEFAULT_ADRESS)