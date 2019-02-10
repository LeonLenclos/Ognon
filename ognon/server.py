"""
This module defines dictionaries, functions and classes to run the ognon servers.
"""

import http.server
import json
import os
import importlib
import threading
import logging

import pythonosc.osc_server
import pythonosc.dispatcher

from . import cursor

functions = {}
cursors = {}

def get_function(path):
    """
    Return a function from the functions dict.

    If the asked function does not exists in the dict, import it, store it in
    the dict and return it.
    """
    try:
        return functions[path]
    except KeyError:
        module_path, fun_name = os.path.split(path.rstrip(os.sep))
        module = importlib.import_module(
            name=module_path.replace(os.sep,'.'),
            package='ognon')
        functions[path] = getattr(module, fun_name)
        return functions[path]

def call_function(path, *args, **kwargs):
    """
    Get a function with get_function, call it with passed args/kwargs and
    return the result.
    """
    def handleError(err_msg):
        logging.warning(err_msg)
        return Exception(err_msg)

    try:
        f = get_function(path)
    except (ImportError, AttributeError):
        return handleError(f'Function not found - {path}')

    try:
        return f(*args, **kwargs)
    except NotImplementedError:
        return handleError(f'Not implemented - {path}')
    except cursor.NoProjectError:
        return handleError('Undefine project')

def get_cursor(name='default'):
    """
    Return a cursor from the cursors dict.

    If the asked cursor does not exists, store a new cursor in the dict and
    return it.
    """
    try:
        return cursors[name]
    except KeyError:
        cursors[name] = cursor.Cursor()
        return cursors[name]


class OgnonHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """
    This class is used to handle the HTTP requests that arrive at the server.

    We wait two kinds of requests :
    
    - GET requests to provide client pages.
    - POST requests to call functions from view or control.
    """

    def log_message(self, format, *args):
        # The default server log is redirected to logging.DEBUG.
        logging.debug(format%args)


    def do_GET(self):
        """
        Handler for GET request.

        append the path to the base url of client files and call the parrent
        do_GET method.
        """
        logging.info(f'http - GET {self.path}')

        baseurl = 'ognon/client'
        # self.path = baseurl + ('/index.html' if self.path == '/' else self.path)
        if self.path.startswith('/docs/'):
            baseurl = ''
        self.path = baseurl + self.path
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
    def do_POST(self):
        """
        Handler for POST request.

        The path tell which function to call. Args are given in the post body.
        Convert the function to json and send it as a response.
        If calling the function raise an exception, send an error message
        """
        logging.info(f'http - POST {self.path}')

        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len).decode('utf-8'))

        cur = get_cursor(post_body.get('cursor'))
        args = post_body.get('args', {})
        reply = call_function(self.path, cur, **args)

        if isinstance(reply, Exception):
            self.send_response(400)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(reply.args[0], 'utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(reply), 'utf-8'))

    def end_headers (self):
        #TODO: check if this is really useful ! 
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET')
        http.server.SimpleHTTPRequestHandler.end_headers(self)


class OgnonOSCDispatcher(pythonosc.dispatcher.Dispatcher):
    """This is the class of the OSC dispatcher."""

    def handlers_for_address(self, address_pattern):
        """yields Handler namedtuples matching the given OSC pattern."""
        logging.info(f'osc - {self.path}')

        def callback(path, cursor_id, *args):
            call_function(path, get_cursor(cursor_id), *args)

        yield pythonosc.dispatcher.Handler(callback, [])


def serve(http_adress, osc_adress, enable_osc=True):
    """
    Serve forever on the given adresses.

    Start to threading servers, an http server and an osc server.
    Set enable_osc to False to disable starting osc server thread.
    """
    dispatcher = OgnonOSCDispatcher()
    osc_server = pythonosc.osc_server.OSCUDPServer(osc_adress, dispatcher)
    osc_server_thread = threading.Thread(target=osc_server.serve_forever)

    http_server = http.server.HTTPServer(http_adress, OgnonHTTPHandler)
    http_server_thread = threading.Thread(target=http_server.serve_forever)

    try :
        if enable_osc:
            osc_server_thread.start()
        http_server_thread.start()
    except KeyboardInterrupt as e:
        print('\n- shutdown -')
        http_server.shutdown()
        osc_server.shutdown()
        raise e