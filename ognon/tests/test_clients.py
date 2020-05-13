from .. import clients

import json

def test_Client(cursor):

	# Test __init__
	client = clients.Client(cursor)
	assert all([state_id is None for key, state_id
		in client.state_identifiers.items()])

	# Test _get_state
	state_ids = client._get_state()
	assert 'proj_state' in state_ids
	assert 'proj_draw_state' in state_ids
	assert 'cursor_state' in state_ids

	# Test update_state
	client.update_state()
	assert all([state_id is not None for key, state_id
		in client.state_identifiers.items()])

	# Test reset_state
	client.reset_state()
	assert all([state_id is None for key, state_id
		in client.state_identifiers.items()])

	# Test compare_state and compare_states
	from ..control import elementsorganizer
	elementsorganizer.add_cell_after(cursor)
	assert not client.compare_state('proj_state')
	elementsorganizer.add_cell_after(cursor)
	assert not client.compare_states(['proj_state', 'proj_draw_state'])


def test_get_client(cursor):
	client_id = clients.new_client(cursor)
	assert type(clients.get_client(client_id)) is clients.Client

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


def test_whats_up(cursor):
	client_id = clients.new_client(cursor)

	# WARNING: weak test
	assert len(clients.whats_up(client_id))
	assert not len(clients.whats_up(client_id))
	# test jsonability
	json.dumps(clients.whats_up(client_id))
