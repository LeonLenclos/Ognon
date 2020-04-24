"""
This module start the server.
"""

import pytest
import argparse
import webbrowser
import logging
import importlib

import ptpython.repl

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
    help='open web browser at the server address')
parser.add_argument(
    '-i', '--interactive',
    action='store_true',
    help='run the interactive Python console')
parser.add_argument(
    '--no-osc',
    action='store_true',
    help='do not start the osc server')
parser.add_argument(
    '-a', '--ip-address',
    type=str,
    help='specify alternate ip address [default: localhost]')
parser.add_argument(
    '-p', '--projects-dir',
    type=str,
    help='specify alternate projects directory [default: {}]'
        .format(PROJECTS_DIR))

# Logging
logging.basicConfig(
    format='%(asctime)s:%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.WARNING
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

    # Open web browser
    if args.interactive:
        interactive()

def interactive():
    """
    The Ognon interactive python console mode allows you to interactively
    use Python commands while running ognon.

    It gives you access to ognon modules :
    - ognon
    - control
    - cursor
    - model
    - projects
    - server
    - tags
    - utils
    - view
    - scripts
    
    And to the cursors dictionnary :
    - cursors
    
    Use quit() for stop serving and quit the REPL.
    """

    # import modules and objects
    import ognon
    from . import control
    from . import cursor
    from . import model
    from . import projects
    from . import server
    from . import tags
    from . import utils
    from . import view
    from . import scripts

    from ognon.server import cursors

    # quit function
    def quit():
        server.stop_serving()
        exit()
    # set logging
    logging.getLogger().setLevel(logging.WARNING)
    # run the repl
    print("\nOgnon interactive python console "
          "(type `help(interactive)` for more information)")
    ptpython.repl.embed(
        globals=globals(),
        locals=locals(),
        # locals={**locals(), **modules},
        title="Ognon",
    )

main(parser.parse_args())
