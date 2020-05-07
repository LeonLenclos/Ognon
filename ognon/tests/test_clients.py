from .. import clients

import json

def test_Client(cursor):

	client = clients.Client(cursor)
	assert all([state_id is None for key, state_id
		in client.state_identifiers.items()])

	client.update_state()
	assert all([state_id is not None for key, state_id
		in client.state_identifiers.items()])

	client.reset_state()
	assert all([state_id is None for key, state_id
		in client.state_identifiers.items()])

	from ..control import elementsorganizer
	elementsorganizer.add_cell_after(cursor)
	assert not client.compare_state('proj_state')
	
def test_new_client(cursor):

	for _ in range(10):
		clients.new_client(cursor)

	old_client_ids = list(clients.clients.keys())
	client_id = clients.new_client(cursor)
	new_client_ids = list(clients.clients.keys())
	assert client_id not in old_client_ids
	assert client_id in new_client_ids

	# test jsonability
	json.dumps(clients.new_client(cursor))

def test_get_client(cursor):
	client_id = clients.new_client(cursor)
	assert type(clients.get_client(client_id)) is clients.Client

def test_smart_view(cursor):
	client_id = clients.new_client(cursor)

	# WARNING: weak test

	# test jsonability
	json.dumps(clients.smart_view(client_id))
