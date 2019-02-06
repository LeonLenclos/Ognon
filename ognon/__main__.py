"""
This module start the server.
"""

import pytest
import argparse
import webbrowser

from . import server
from . import __version__, PROJECTS_DIR, DEFAULT_ADRESS


parser = argparse.ArgumentParser(
	prog='python -m ognon',
	description='Start the Ognon server.')
parser.add_argument('-t', '--test',
	action='store_true',
	help='run tests and exit')
parser.add_argument('-b', '--browse',
	action='store_true',
	help='open the adress in a web browser')

def main(args):
	if args.test:
		return pytest.main(['-x', 'ognon/tests'])

	title = ' Ognon v{} '.format(__version__)
	print('+{line}+\n|{title}|\n+{line}+'.format(line='-'*len(title), title=title))
	print("Working on file://{}".format(PROJECTS_DIR))
	print("Serving on http://{}:{}".format(*DEFAULT_ADRESS))

	if args.browse:
		webbrowser.open_new("http://{}:{}".format(*DEFAULT_ADRESS))

	server.serve(DEFAULT_ADRESS)

main(parser.parse_args())
