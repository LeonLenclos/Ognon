"""
This module defines dictionaries, functions and classes to run the ognon server.
"""

import http.server
import json
import importlib

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
        splited = path.strip('/').split('/')
        module_path, fun_name = '.'.join(splited[:-1]), splited[-1]
        module = importlib.import_module('.' + module_path, package='ognon')
        functions[path] = getattr(module, fun_name)
        return functions[path]

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

class OgnRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    This class is used to handle the HTTP requests that arrive at the server.

    We wait two kinds of requests :
    
    - GET requests to provide client pages.
    - POST requests to call functions from view or control.
    """

    def do_GET(self):
        """
        Handler for GET request.

        append the path to the base url of client files and call the parrent
        do_GET method.
        """
        baseurl = 'ognon/client'
        self.path = baseurl + ('/index.html' if self.path == '/' else self.path)
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
    def do_POST(self):
        """
        Handler for POST request.

        The path tell which function to call. Args are given in the post body.
        Convert the function to json and send it as a response.
        If calling the function raise an exception, send an error message
        """
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len).decode('utf-8'))

        cur = get_cursor(post_body.get('cursor'))
        args = post_body.get('args', {})
        fun = get_function(self.path)

        try:
            reply = fun(cur, **args)
            self.send_response(200)
        except Exception as e:
            reply = {'err': e}
            self.send_response(400)
            raise

        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(reply), 'utf-8'))

    def end_headers (self):
        #TODO: check if this is really useful ! 
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

def serve(adress):
    """
    Serve forever on the given adress.
    """
    server = http.server.HTTPServer(adress, OgnRequestHandler)
    server.serve_forever()
