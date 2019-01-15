#! /usr/bin/python3
# coding: utf8

"""
Run this script (as root) to run the server.

"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

import ognon


class OgnRequestHandler(BaseHTTPRequestHandler):

    _projects = {}

    def get_project(self, project_name):
        """ 
        Get a project by its name.
        If the project is not in the _projects dict, create it.
        """
        try:
            return self._projects[project_name]
        except KeyError:
            self._projects[project_name] = ognon.OgnProject(project_name)
            return self._projects[project_name]

    def ask_project(self, project_name, request):
        """
        Send the request to the project
        """
        return self.get_project(project_name).ask(request)

    def do_GET(self):
        """
        Handler for GET request
        / -> www/index.html
        /*.html -> www/*.html
        /*.css -> www/*.css
        /*.js -> www/*.js
        /*.ico -> www/*.ico
        /*.gif -> a gif render of the * project
        /* -> www/project.html formated with the * project name
        """

        get_page = lambda page: open("www" + page).read()
        # Try to open asked path
        try:
            if self.path == '/':
                data = get_page('/index.html')

            elif (self.path.endswith('.html')
               or self.path.endswith('.map')
               or self.path.endswith('.js')
               or self.path.endswith('.css')):
                data = get_page(self.path)

            elif self.path.endswith('.ico'):
                data = open("www" + self.path, 'rb').read()

            elif self.path.endswith('.gif'):
                project = self.get_project(self.path[:-4])
                data = project.get_gif()

            elif self.path.startswith('/project/'):
                project_name = self.path[len('/project/'):]
                project = self.get_project(project_name)
                data = get_page('/project.html').format(project=project_name)

            elif self.path.startswith('/export/'):
                project_name = self.path[len('/export/'):]
                project = self.get_project(project_name)
                data = get_page('/export.html').format(project=project_name)

            elif self.path.startswith('/config/'):
                project_name = self.path[len('/config/'):]
                project = self.get_project(project_name)
                data = get_page('/config.html').format(project=project_name)

            elif self.path.startswith('/edit/'):
                project_name = self.path[len('/edit/'):]
                project = self.get_project(project_name)
                data = get_page('/edit.html').format(project=project_name)

            else: raise FileNotFoundError

            self.send_response(200)
        except FileNotFoundError as e:
            print(e)
            data = "File not found :("
            self.send_response(404)

        # Return asked page
        self.end_headers()
        if type(data) is str:
            data = bytes(data, 'utf-8')
        self.wfile.write(data)

    def do_POST(self):
        """Handler for POST request"""

        project_name = self.path[1:]
        project = self.get_project(project_name)

        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len).decode('utf-8'))

        reply = self.ask_project(project_name, post_body)


        # return asked data
        if reply:
            self.send_response(200)
        else:
            self.send_response(400)
            reply = {'err': "Bad request..."}

        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(reply), 'utf-8'))

    def end_headers (self):
        #TODO: check if this is really useful ! 
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        BaseHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    ip = ognon.OgnProject.default_config['server']['ip']
    port = int(ognon.OgnProject.default_config['server']['port'])
    server = HTTPServer((ip, port), OgnRequestHandler)
    print("serving on {}:{}".format(ip, port))
    server.serve_forever()
