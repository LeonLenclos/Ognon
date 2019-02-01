from .. import view

def test_get_path(cursor):
	import os
	path = view.get_path(cursor)
	assert path
	assert view.get_path(cursor, 'foo').startswith(path)
