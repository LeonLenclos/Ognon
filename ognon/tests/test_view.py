from .. import view
import json

def test_get_path(cursor):
	import os
	path = view.get_path(cursor)
	assert path
	assert view.get_path(cursor, 'foo').startswith(path)

	# test jsonability
	json.dumps(view.get_path(cursor))

def test_get_projects_tree(cursor):
	# WARNING: weak test
	
	# test jsonability
	json.dumps(view.get_projects_tree(cursor))

def test_get_projects(cursor):
	# WARNING: weak test
	
	# test jsonability
	json.dumps(view.get_projects_tree(cursor))

def test_get_view_config(cursor):

	assert view.get_view_config(cursor) == cursor.proj.config['view']	
	# test jsonability
	json.dumps(view.get_view_config(cursor))

def test_get_config(cursor):
	# test jsonability
	json.dumps(view.get_config(cursor))


def test_get_anims(cursor):	
	for a in view.get_anims(cursor):
		assert a in cursor.proj.anims
		
	# test jsonability
	json.dumps(view.get_anims(cursor))

def test_get_playing(cursor):
	assert isinstance(view.get_playing(cursor), bool)
	# test jsonability
	json.dumps(view.get_playing(cursor))

def test_get_timeline(cursor):
	
	assert 'len' in view.get_timeline(cursor)
	assert len(view.get_timeline(cursor)['layers']) == len(cursor.get_anim().layers)
	assert view.get_timeline(cursor)['layers'][0][0] == view.get_element_infos(cursor, layer=0, frm=0)
	# test jsonability
	json.dumps(view.get_timeline(cursor))

def test_get_cursor_infos(cursor):
	
	for key in ('project_name', 'playing', 'clipboard', 'anim', 'frm', 'layer'):
		assert key in view.get_cursor_infos(cursor)	
	# test jsonability
	json.dumps(view.get_cursor_infos(cursor))

def test_get_element_infos(cursor):
	
	for key in ('type', 'len', 'tags', 'name'):
		assert key in view.get_element_infos(cursor)	
	# test jsonability
	json.dumps(view.get_element_infos(cursor))

def test_get_lines(cursor):
	from ..control import drawer
	line = [0,0,10,10,0,10]
	drawer.draw(cursor, line)
	assert line in [line['coords'] for line in view.get_lines(cursor)]

	# test draft mode
	from ..control import tagger
	tagger.add_tag(cursor, 'draft')
	assert line not in [line['coords'] for line in view.get_lines(cursor, playing=True)]
	assert line in [line['coords'] for line in view.get_lines(cursor, playing=False)]

	# weak test on animref
	cursor.set_pos(anim='testing-anim-with-animref',frm=5)
	view.get_lines(cursor)

	# weak test on empty anim
	cursor.set_pos(anim='empty-anim')
	view.get_lines(cursor)
	cursor.set_pos(anim='really-empty-anim')
	view.get_lines(cursor)

	
	# test jsonability
	from .. import utils
	json.dumps(view.get_lines(cursor), cls=utils.SetEncoder)


def test_get_onion_skin(cursor):
	# WARNING: weak test
	from ..control import drawer
	line = [0,0,10,10,0,10]
	drawer.draw(cursor, line)
	# test jsonability
	from .. import utils
	json.dumps(view.get_onion_skin(cursor), cls=utils.SetEncoder)
