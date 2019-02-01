from .. import control

def test_animsmanager(cursor):

	# new_anim
	assert control.animsmanager.new_anim(cursor, 'fresh-new-anim') is None
	assert 'fresh-new-anim' in cursor.proj.anims
	assert cursor.get_pos('anim') == 'fresh-new-anim'

	#  select_anim
	assert control.animsmanager.select_anim(cursor, 'master') is None
	assert cursor.get_pos('anim') == 'master'

	# del_anim
	assert control.animsmanager.del_anim(cursor, 'fresh-new-anim') is None
	assert 'fresh-new-anim' not in cursor.proj.anims

def test_navigator(cursor):

	# run & play
	assert control.navigator.run(cursor) is None
	assert cursor.playing is False
	assert cursor.get_pos('frm') == 0

	assert control.navigator.play(cursor) is None
	assert cursor.playing is True
	assert cursor.get_pos('frm') == 0

	assert control.navigator.run(cursor) is None
	assert cursor.playing is True
	assert cursor.get_pos('frm') == 1

	assert control.navigator.play(cursor) is None
	assert cursor.playing is False
	assert cursor.get_pos('frm') == 1

	# TODO: WARNING ! auto_run NOT TESTED

	# prev_frm
	cursor.loop = False
	assert control.navigator.prev_frm(cursor) is None
	assert cursor.get_pos('frm') == 0
	assert control.navigator.prev_frm(cursor) is None
	assert cursor.get_pos('frm') == 0
	cursor.loop = True
	assert control.navigator.prev_frm(cursor) is None
	assert cursor.get_pos('frm') == 1

	# next_frm
	cursor.loop = False
	assert control.navigator.next_frm(cursor) is None
	assert cursor.get_pos('frm') == 1
	assert control.navigator.next_frm(cursor) is None
	assert cursor.get_pos('frm') == 1
	cursor.loop = True
	assert control.navigator.next_frm(cursor) is None
	assert cursor.get_pos('frm') == 0

	# last_frm
	assert control.navigator.last_frm(cursor) is None
	assert cursor.get_pos('frm') == 1

	# first_frm
	assert control.navigator.first_frm(cursor) is None
	assert cursor.get_pos('frm') == 0

	# go_to_frm
	assert control.navigator.go_to_frm(cursor, 1) is None
	assert cursor.get_pos('frm') == 1

	# go_to_layer
	assert control.navigator.go_to_layer(cursor, 1) is None
	assert cursor.get_pos('layer') == 1


def test_organizer(cursor):
	from .. import model

	class DebugCell(model.Cell):
		def __init__(self, debug):
			super().__init__()
			self.debug = debug
			
	def debugs_list(cursor):
		return [c.debug if type(c) is DebugCell else None for c in cursor.get_layer().elements]

	def init_orga(cursor):
		control.navigator.first_frm(cursor)
		cursor.get_layer().elements = [DebugCell(i) for i in range(5)]

	# add_element_after
	init_orga(cursor)
	assert control.organizer.add_element_after(cursor, DebugCell('new')) is None
	assert debugs_list(cursor) == [0,'new',1,2,3,4]
	assert cursor.get_pos('frm') == 1

	control.navigator.last_frm(cursor)
	assert control.organizer.add_element_after(cursor, DebugCell('new')) is None
	assert debugs_list(cursor) == [0,'new',1,2,3,4,'new']
	assert cursor.get_pos('frm') == 6

	# add_element_before
	init_orga(cursor)
	assert control.organizer.add_element_before(cursor, DebugCell('new')) is None
	assert debugs_list(cursor) == ['new',0,1,2,3,4]
	assert cursor.get_pos('frm') == 0

	# add_cell_after & add_cell_before
	assert control.organizer.add_cell_before(cursor) is None
	assert isinstance(cursor.get_element(), model.Cell)
	assert control.organizer.add_cell_after(cursor) is None
	assert isinstance(cursor.get_element(), model.Cell)

	# add_animref_after & add_animref_before
	assert control.organizer.add_animref_before(cursor, 'testing-anim') is None
	assert isinstance(cursor.get_element(), model.AnimRef)
	assert control.organizer.add_animref_after(cursor, 'testing-anim') is None
	assert isinstance(cursor.get_element(), model.AnimRef)

	# del_element
	init_orga(cursor)
	assert control.organizer.del_element(cursor) is None
	assert debugs_list(cursor) == [1,2,3,4]
	assert cursor.get_pos('frm') == 0
	assert control.organizer.del_element(cursor) is None
	assert debugs_list(cursor) == [2,3,4]
	assert cursor.get_pos('frm') == 0
	control.navigator.last_frm(cursor)
	assert control.organizer.del_element(cursor) is None
	assert debugs_list(cursor) == [2,3]
	assert cursor.get_pos('frm') == 1

	# move_element_forward
	init_orga(cursor)
	assert control.organizer.move_element_forward(cursor) is None
	assert debugs_list(cursor) == [1,0,2,3,4]
	assert cursor.get_pos('frm') == 1
	assert control.organizer.move_element_forward(cursor) is None
	assert debugs_list(cursor) == [1,2,0,3,4]
	assert cursor.get_pos('frm') == 2
	control.navigator.last_frm(cursor)
	assert control.organizer.move_element_forward(cursor) is None
	assert debugs_list(cursor) == [1,2,0,3,4]
	assert cursor.get_pos('frm') == 4

	# move_element_backward
	init_orga(cursor)
	assert control.organizer.move_element_backward(cursor) is None
	assert debugs_list(cursor) == [0,1,2,3,4]
	assert cursor.get_pos('frm') == 0
	control.navigator.last_frm(cursor)
	assert control.organizer.move_element_backward(cursor) is None
	assert debugs_list(cursor) == [0,1,2,4,3]
	assert cursor.get_pos('frm') == 3
	assert control.organizer.move_element_backward(cursor) is None
	assert debugs_list(cursor) == [0,1,4,2,3]
	assert cursor.get_pos('frm') == 2

	# add_layer
	assert control.organizer.add_layer(cursor) is None
	assert len(cursor.get_anim().layers) == 3

def test_projectmanager(cursor):
	import os
	from ..view import get_path
	# load
	assert control.projectmanager.load(cursor, 'fresh_new_project') is None
	assert cursor.proj.name == 'fresh_new_project'
	assert os.path.isdir(get_path(cursor))

	# assert control.projectmanager.load(cursor, 'testing') is None
	# assert cursor.proj.name == 'testing'
	# assert 'testing-anim' in cursor.proj.anims

	# save
	control.projectmanager.load(cursor, 'testing')
	control.animsmanager.new_anim(cursor, 'new_anim_to_be_saved')
	assert control.projectmanager.save(cursor) is None
	control.projectmanager.load(cursor, 'another_project')
	control.projectmanager.load(cursor, 'testing')
	assert 'new_anim_to_be_saved' in cursor.proj.anims

	# clean
	import shutil
	control.projectmanager.load(cursor, 'fresh_new_project')
	shutil.rmtree(get_path(cursor))
	control.projectmanager.load(cursor, 'another_project')
	shutil.rmtree(get_path(cursor))
	control.projectmanager.load(cursor, 'testing')
	shutil.rmtree(get_path(cursor))