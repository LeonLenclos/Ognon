"""
This module start the server.
"""

import pytest
import argparse
import webbrowser
import logging

from . import server
from . import __version__, PROJECTS_DIR, HTTP_ADRESS, OSC_ADRESS

# Parsing command line args
parser = argparse.ArgumentParser(
	prog='python -m ognon',
	description='Start the Ognon server.')
parser.add_argument(
	'-t', '--test',
	action='store_true',
	help='run tests and exit')
parser.add_argument(
	'-b', '--browse',
	action='store_true',
	help='open the adress in a web browser')
parser.add_argument(
	'--no-osc',
	action='store_true',
	help='also serve osc on another port.')
parser.add_argument(
	'--ip-adress',
	type=str,
	help='set a different server ip adress.')
parser.add_argument(
	'--projects-dir',
	type=str,
	help='set a different projects directory.')

# Logging
logging.basicConfig(
	format='%(asctime)s:%(msecs)03d %(levelname)s: %(message)s',
	datefmt='%H:%M:%S',
	level=logging.INFO
)

def main(args):
	global HTTP_ADRESS, OSC_ADRESS, PROJECTS_DIR
	
	# Test
	if args.test:
		return pytest.main(['-x', 'ognon/tests'])

	# Print version
	title = ' Ognon v{} '.format(__version__)
	print('+{line}+\n|{title}|\n+{line}+'.format(line='-'*len(title), title=title))
	
	# Projects directory
	if args.projects_dir:
		PROJECTS_DIR = args.projects_dir
	print("Working on file://{}".format(PROJECTS_DIR))

	# Ip adress
	if args.ip_adress:
		HTTP_ADRESS = args.ip_adress, HTTP_ADRESS[1]
		OSC_ADRESS = args.ip_adress, OSC_ADRESS[1]

	# Run Servers
	server.serve(HTTP_ADRESS, OSC_ADRESS, not args.no_osc)
	print("Serving on http://{}:{}".format(*HTTP_ADRESS))
	if not args.no_osc:
		print("Serving on osc://{}:{}".format(*OSC_ADRESS))

	# Open web browser
	if args.browse:
		webbrowser.open_new("http://{}:{}".format(*HTTP_ADRESS))


main(parser.parse_args())
