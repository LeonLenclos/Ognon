from ..control import animsmanager

def test_new_anim(cursor):

	assert animsmanager.new_anim(cursor, 'fresh-new-anim') is None
	assert 'fresh-new-anim' in cursor.proj.anims
	assert cursor.get_pos('anim') == 'fresh-new-anim'

def test_select_anim(cursor):

	assert animsmanager.select_anim(cursor, 'testing-anim') is None
	assert cursor.get_pos('anim') == 'testing-anim'
	assert animsmanager.select_anim(cursor, 'master') is None
	assert cursor.get_pos('anim') == 'master'
	assert animsmanager.select_anim(cursor, 'unexisting-anim') is None
	assert cursor.get_pos('anim') == 'master'

def test_del_anim(cursor):

	assert animsmanager.del_anim(cursor, 'testing-anim') is None
	assert 'testing-anim' not in cursor.proj.anims
