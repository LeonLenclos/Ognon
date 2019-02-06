from .. import control
from .. import model

def test_add_layer(cursor):
	assert control.layersorganizer.add_layer(cursor) is None
	assert len(cursor.get_anim().layers) == 3

def test_del_layer(cursor):
	assert control.layersorganizer.del_layer(cursor) is None
	assert len(cursor.get_anim().layers) == 1

def test_move_layer_up(cursor):
	cursor.set_pos(layer=1)
	excepted_state = [cursor.get_anim().layers[1], cursor.get_anim().layers[0]]
	assert control.layersorganizer.move_layer_up(cursor) is None
	assert cursor.get_anim().layers == excepted_state

def test_move_layer_down(cursor):
	excepted_state = [cursor.get_anim().layers[1], cursor.get_anim().layers[0]]
	assert control.layersorganizer.move_layer_down(cursor) is None
	assert cursor.get_anim().layers == excepted_state

def test__pop_layer_at(cursor):
	layer = cursor.get_anim().layers[0]
	assert control.layersorganizer._pop_layer_at(cursor, 0) is layer
	assert len(cursor.get_anim().layers) == 1
