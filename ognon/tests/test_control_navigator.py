from ..control import navigator
from .. import view

def test_run_and_play(cursor):

	# run & play
	assert navigator.run(cursor) is None
	assert cursor.playing is False
	assert cursor.get_pos('frm') == 0

	assert navigator.play(cursor) is None
	assert cursor.playing is True
	assert cursor.get_pos('frm') == 0

	assert navigator.run(cursor) is None
	assert cursor.playing is True
	assert cursor.get_pos('frm') == 1

	assert navigator.play(cursor) is None
	assert cursor.playing is False
	assert cursor.get_pos('frm') == 1

# TODO: WARNING ! auto_run NOT TESTED

def test_prev_frm(cursor):
	assert cursor.get_pos('anim') == 'master'
	assert cursor.anim_len() == 2
	cursor.proj.config['play']['loop'] = False
	assert navigator.prev_frm(cursor) is None
	assert cursor.get_pos('frm') == 0
	assert navigator.prev_frm(cursor) is None
	assert cursor.get_pos('frm') == 0
	cursor.proj.config['play']['loop'] = True
	assert navigator.prev_frm(cursor) is None
	assert cursor.get_pos('frm') == 1

def test_next_frm(cursor):
	cursor.proj.config['play']['loop'] = False
	assert navigator.next_frm(cursor) is None
	assert cursor.get_pos('frm') == 1
	assert navigator.next_frm(cursor) is None
	assert cursor.get_pos('frm') == 1
	cursor.proj.config['play']['loop'] = True
	assert navigator.next_frm(cursor) is None
	assert cursor.get_pos('frm') == 0

def test_last_frm(cursor):
	assert navigator.last_frm(cursor) is None
	assert cursor.get_pos('frm') == 1

def test_first_frm(cursor):
	assert navigator.first_frm(cursor) is None
	assert cursor.get_pos('frm') == 0

def test_go_to_frm(cursor):
	assert navigator.go_to_frm(cursor, 1) is None
	assert cursor.get_pos('frm') == 1

def test_go_to_layer(cursor):
	assert navigator.go_to_layer(cursor, 1) is None
	assert cursor.get_pos('layer') == 1

def test_lower_layer(cursor):
	cursor.set_pos(anim="testing-layers")
	navigator.go_to_layer(cursor, 1)
	assert navigator.lower_layer(cursor) is None
	assert cursor.get_pos('layer') == 2
	assert navigator.lower_layer(cursor) is None
	assert cursor.get_pos('layer') == 0

def test_upper_layer(cursor):
	cursor.set_pos(anim="testing-layers")
	navigator.go_to_layer(cursor, 1)
	assert navigator.upper_layer(cursor) is None
	assert cursor.get_pos('layer') == 0
	assert navigator.upper_layer(cursor) is None
	assert cursor.get_pos('layer') == 2
