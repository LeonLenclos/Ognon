"""
This module start the server.
"""

import pytest
import argparse
import webbrowser

from . import server
from . import __version__, PROJECTS_DIR, DEFAULT_ADRESS, DEFAULT_OSC_ADRESS


parser = argparse.ArgumentParser(
	prog='python -m ognon',
	description='Start the Ognon server.')
parser.add_argument('-t', '--test',
	action='store_true',
	help='run tests and exit')
parser.add_argument('-b', '--browse',
	action='store_true',
	help='open the adress in a web browser')
parser.add_argument('--no-osc',
	action='store_true',
	help='also serve osc on another port.')

def main(args):
	if args.test:
		return pytest.main(['-x', 'ognon/tests'])

	title = ' Ognon v{} '.format(__version__)
	print('+{line}+\n|{title}|\n+{line}+'.format(line='-'*len(title), title=title))
	print("Working on file://{}".format(PROJECTS_DIR))

	if args.browse:
		webbrowser.open_new("http://{}:{}".format(*DEFAULT_ADRESS))

	server.serve(DEFAULT_ADRESS, DEFAULT_OSC_ADRESS, not args.no_osc)
	print("Serving on http://{}:{}".format(*DEFAULT_ADRESS))
	print("Serving on osc://{}:{}".format(*DEFAULT_OSC_ADRESS))

main(parser.parse_args())
