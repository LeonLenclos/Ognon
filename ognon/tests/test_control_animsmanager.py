from ..control import animsmanager

def test_new_anim(cursor):

	assert animsmanager.new_anim(cursor, 'fresh-new-anim') is None
	assert 'fresh-new-anim' in cursor.proj.anims

def test_select_anim(cursor):

	assert animsmanager.select_anim(cursor, 'testing-anim') is None
	assert cursor.get_pos('anim') == 'testing-anim'
	assert animsmanager.select_anim(cursor, 'master') is None
	assert cursor.get_pos('anim') == 'master'
	assert animsmanager.select_anim(cursor, 'unexisting-anim') is None
	assert cursor.get_pos('anim') == 'unexisting-anim'

def test_del_anim(cursor):

	assert animsmanager.del_anim(cursor, 'testing-anim') is None
	assert 'testing-anim' not in cursor.proj.anims

def test_new_animref(cursor):

	_, e, _ = cursor.get_element_pos()
	assert animsmanager.new_animref(cursor, 'fresh-new-animref') is None
	assert 'fresh-new-animref' in cursor.proj.anims
	_, e_in_anim, _ = cursor.get_element_pos(anim='fresh-new-animref', layer=0, frm=0)
	assert e_in_anim == e

	_, e, _ = cursor.get_element_pos()
	assert e.name == 'fresh-new-animref'

def test_select_animref(cursor):

	cursor.set_pos(anim='testing-anim-with-animref', layer=0, frm=1)
	assert animsmanager.select_animref(cursor) is None
	assert cursor.get_pos('anim') == 'long-anim'
