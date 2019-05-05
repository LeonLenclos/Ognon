from ..control import *

def test_change_project_state(cursor):

	@change_project_state
	def control_function(cursor):
		pass

	state_id = cursor.proj.state_id
	control_function(cursor)

	assert state_id + 1 == cursor.proj.state_id

