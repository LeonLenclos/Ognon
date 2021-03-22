import pytest

from ..control import projectmanager
from .. import view
from .. import projects
import os

proj_dir = projects.PROJECTS_DIR = view.PROJECTS_DIR = '/tmp/ogn/ognons/'
if not os.path.isdir(proj_dir):
	os.makedirs(proj_dir)

def test_get(cursor):

	assert projectmanager.get(cursor, 'fresh_new_project') is None
	assert cursor.proj.name == 'fresh_new_project'

def test_load(cursor):
	with pytest.raises(projectmanager.ProjectNotFoundError):
		projectmanager.load(cursor, 'unexisting_project_to_load')

	os.mkdir(proj_dir + 'project_on_disk')
	assert projectmanager.load(cursor, 'project_on_disk') is None
	assert cursor.proj.name == 'project_on_disk'


def test_save(cursor):

	from ..control import animsmanager

	projectmanager.get(cursor, 'testing')
	animsmanager.new_anim(cursor, 'new_anim_to_be_saved')
	assert projectmanager.save(cursor) is None
	projectmanager.get(cursor, 'another_project')
	projectmanager.get(cursor, 'testing')
	assert 'new_anim_to_be_saved' in cursor.proj.anims
	assert os.path.isdir(view.get_path(cursor))
