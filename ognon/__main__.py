"""
This module start the server.
"""

import pytest
import argparse
import webbrowser
import logging

from . import utils
from . import server
from . import __version__, PROJECTS_DIR, HTTP_ADDRESS, OSC_ADDRESS

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
	help='open the address in a web browser')
parser.add_argument(
	'--no-osc',
	action='store_true',
	help='also serve osc on another port.')
parser.add_argument(
	'--ip-address',
	type=str,
	help='set a different server ip address.')
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
	global HTTP_ADDRESS, OSC_ADDRESS, PROJECTS_DIR

	# Test
	if args.test:
		return pytest.main(['-x', utils.pkgabspath('tests')])

	# Print version
	title = ' Ognon v{} '.format(__version__)
	print('+{line}+\n|{title}|\n+{line}+'.format(line='-'*len(title), title=title))
	
	# Projects directory
	if args.projects_dir:
		PROJECTS_DIR = args.projects_dir
	print("Working on file://{}".format(PROJECTS_DIR))

	# Ip address
	if args.ip_address:
		HTTP_ADDRESS = args.ip_address, HTTP_ADDRESS[1]
		OSC_ADDRESS = args.ip_address, OSC_ADDRESS[1]

	# Run Servers
	server.serve(HTTP_ADDRESS, OSC_ADDRESS, not args.no_osc)
	print("Serving on http://{}:{}".format(*HTTP_ADDRESS))
	if not args.no_osc:
		print("Serving on osc://{}:{}".format(*OSC_ADDRESS))

	# Open web browser
	if args.browse:
		webbrowser.open_new("http://{}:{}".format(*HTTP_ADDRESS))


main(parser.parse_args())
