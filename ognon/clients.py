"""
This module is the clients handler.

The purpose of these features is to keep track of how much a client knows about
the cursor he is working on. Thus, it is not necessary to send him information
he already knows.
"""

from . import view

clients = {}

class Client():
    """
    This class describe Client
    
    A Client has a cursor and a state_identifiers dict.
    """
    def __init__(self, cursor):
        """Init a Client with a cursor."""
        self.cursor = cursor
        self.reset_state()

    def _get_state(self):
        """Return the current state of the cursor"""
        proj_name = self.cursor.proj.name
        anim_name = self.cursor.get_pos('anim')
        return {
            'proj_state': proj_name +anim_name+ str(self.cursor.proj.state_id),
            'proj_draw_state': proj_name +anim_name+ str(self.cursor.proj.draw_state_id),
            'cursor_state':self.cursor.state_id,
        }

    def update_state(self):
        """Update state_identifiers from get_state"""
        self.state_identifiers.update(self._get_state())

    def reset_state(self):
        """Reset state_identifiers to None"""
        self.state_identifiers = {k:None for k in self._get_state()}

    def compare_state(self, state_key):
        """
        Return true if the stored state id is the same that cursor state id
        for a given state_key.
        """
        return self._get_state()[state_key] == self.state_identifiers[state_key]

    def compare_states(self, state_keys):
        """
        Return true if the stored states id are the same that cursor states id
        for a given state_key list.
        """
        return all(self.compare_state(k) for k in state_keys)

def get_client(client_id):
    """Return a client from the client dict"""
    return clients[client_id]

def new_client(cursor):
    """
    Create a client id, store it in the clients dict with a Client instance.

    Return the created client id.
    """
    # find a client_id that does not exists in clients
    client_id = 0
    while client_id in clients:
        client_id += 1

    clients[client_id] = Client(cursor)

    return client_id


whats_up_content = {
    'drawing': {
        'view_function':view.get_drawing,
        'change_with':['proj_state', 'proj_draw_state', 'cursor_state']
    },
    'timeline':{
        'view_function':view.get_timeline,
        'change_with':['proj_state']
    },
    'cursor_infos':{
        'view_function':view.get_cursor_infos,
        'change_with':['cursor_state']
    },
    'element_infos':{
        'view_function':view.get_element_infos,
        'change_with':['proj_state', 'cursor_state']
    },
    'config':{
        'view_function':view.get_config,
        'change_with':['proj_state']
    },
}

def whats_up(client_id):
    """
    Returns a dict that contains all the information a client web app needs
    to update.
    """
    client = get_client(client_id)
    view_value = {}
    for k, v in whats_up_content.items():
        if not client.compare_states(v['change_with']):
            view_value[k]=v['view_function'](client.cursor)
    client.update_state()
    return view_value


