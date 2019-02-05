from ..control import projectmanager
from .. import view
from .. import projects
import os

proj_dir = projects.PROJECTS_DIR = view.PROJECTS_DIR = '/tmp/ogn/ognons/'
if not os.path.isdir(proj_dir):
	os.makedirs(proj_dir)

def test_load(cursor):

	import os

	assert projectmanager.load(cursor, 'fresh_new_project') is None
	assert cursor.proj.name == 'fresh_new_project'


def test_save(cursor):

	from ..control import animsmanager

	projectmanager.load(cursor, 'testing')
	animsmanager.new_anim(cursor, 'new_anim_to_be_saved')
	assert projectmanager.save(cursor) is None
	projectmanager.load(cursor, 'another_project')
	projectmanager.load(cursor, 'testing')
	assert 'new_anim_to_be_saved' in cursor.proj.anims
	assert os.path.isdir(view.get_path(cursor))
