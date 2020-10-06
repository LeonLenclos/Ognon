from ..control import *

def test_change_cursor_state(cursor):

    @change_cursor_state
    def control_function(cursor):
        pass

    state_id = cursor.state_id
    control_function(cursor)

    assert state_id + 1 == cursor.state_id


def test_change_project_state(cursor):

    @change_project_state
    def control_function(cursor):
        pass

    state_id = cursor.proj.state_id
    control_function(cursor)

    assert state_id + 1 == cursor.proj.state_id


def test_change_project_draw_state(cursor):

    @change_project_draw_state
    def control_function(cursor):
        pass

    state_id = cursor.proj.draw_state_id
    control_function(cursor)

    assert state_id + 1 == cursor.proj.draw_state_id

