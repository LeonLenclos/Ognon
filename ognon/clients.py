"""
This module is the clients handler.
"""

from . import view

clients = {}

class Client():
    """Client"""
    def __init__(self, cursor):
        self.cursor = cursor
        self.reset_state()

    def get_state(self):
        return {
            'proj_name':self.cursor.proj.name,
            'proj_state':self.cursor.proj.state_id,
            'proj_draw_state':self.cursor.proj.draw_state_id,
            'cursor_pos':'{anim}-{layer}-{frm}'.format(**self.cursor.get_pos()),
        }

    def update_state(self):
        self.state_identifiers.update(self.get_state())

    def reset_state(self):
        self.state_identifiers = {k:None for k in self.get_state()}

    def compare_state(self, state_key):
        return self.get_state()[state_key] == self.state_identifiers[state_key]

    def compare_states(self, state_keys):
        return all(self.compare_state(k) for k in state_keys)

def get_client(client_id):
    return clients[client_id]

def new_client(cursor):
    """
    Create a client identifiant, store it in the clients dict and return it.
    """
    # generate a client_id that does not exists in clients
    client_id = 0
    while client_id in clients:
        client_id += 1

    clients[client_id] = Client(cursor)

    return client_id

def smart_view(client_id):
    client = get_client(client_id)
    view_value = {}
    view_value['lines'] = None if client.compare_states([
            'proj_name',
            'proj_state',
            'proj_draw_state',
            'cursor_pos',
        ]) else view.get_lines(client.cursor)

    view_value['timeline'] = None if client.compare_states([
            'proj_name',
            'proj_state',
        ]) else view.get_timeline(client.cursor)

    view_value['cursor_infos'] = None if client.compare_states([
            'proj_name',
            'cursor_pos',
        ]) else view.get_cursor_infos(client.cursor)

    view_value['element_infos']  = None if client.compare_states([
            'proj_name',
            'proj_state',
            'cursor_pos',
        ]) else view.get_element_infos(client.cursor)

    client.update_state()
    return view_value