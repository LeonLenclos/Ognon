"""
This module defines the ognon http server
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
import json
from importlib import import_module

from .cursor import Cursor

functions = {}
def get_function(path):
    path = path.strip('/').split('/')
    py_path = '.'.join(path)
    module_path = '.'.join(path[:-1])
    fun_name = path[-1]
    try:
        return functions[py_path]
    except KeyError:
        module = import_module('.'+module_path, package='ognon')
        functions[py_path] = getattr(module, fun_name)
        return functions[py_path]

class OgnRequestHandler(SimpleHTTPRequestHandler):

    cursors = {}

    def do_GET(self):
        """
        Handler for GET request
        """
        if self.path == '/' :
            self.path += 'index.html'
        self.path = 'ognon/www' + self.path
        SimpleHTTPRequestHandler.do_GET(self)
        
    def do_POST(self):
        """Handler for POST request"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len).decode('utf-8'))

        cursor_name = post_body.get('cursor', 'default')
        try:
            cursor = self.cursors[cursor_name]
        except KeyError:
            cursor = self.cursors[cursor_name] = Cursor()

        args = post_body.get('args', {})
        fun = get_function(self.path)
        try:
            reply = fun(cursor, **args)
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
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        SimpleHTTPRequestHandler.end_headers(self)

def serve(adress):
    server = HTTPServer(adress, OgnRequestHandler)
    server.serve_forever()
