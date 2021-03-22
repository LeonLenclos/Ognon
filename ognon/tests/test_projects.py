import pytest, os
from .. import projects
from .. import model

proj_dir = projects.PROJECTS_DIR = '/tmp/ogn/ognons/'
# if not os.path.isdir(proj_dir):
# 	os.makedirs(proj_dir)

def test_get_saved_projects_list():

	projects.get_saved_projects_list()
	
	os.mkdir(proj_dir + "dir1")
	os.mkdir(proj_dir + "dir2")
	os.mkdir(proj_dir + "_dir3")
	os.mkdir(proj_dir + ".dir4")

	assert 'dir1' in projects.get_saved_projects_list()
	assert 'dir2' in projects.get_saved_projects_list()
	assert '_dir3' not in projects.get_saved_projects_list()
	assert '.dir4' not in projects.get_saved_projects_list()

def test_save_project_at():
	os.mkdir('/tmp/ogn/some_dir/')

	proj = model.Project('a_project')
	proj.config['a_section'] = {'an_option':'a value'}
	proj.anims['an_anim'] = model.Anim
	
	projects.save_project_at(proj, '/tmp/ogn/some_dir/my_project/')

	assert os.path.isdir('/tmp/ogn/some_dir/my_project/')
	assert os.path.isfile('/tmp/ogn/some_dir/my_project/an_anim.ogn')
	assert os.path.isdir('/tmp/ogn/some_dir/my_project/export/')
	assert os.path.isfile('/tmp/ogn/some_dir/my_project/config.ini')

def test_save():
	projects.save(model.Project('hello'))
	assert os.path.isdir(proj_dir + 'hello/')

def test_new():
	proj = projects.new('my_new_project')

	assert proj.name == 'my_new_project'
	assert isinstance(proj, model.Project) 
	assert projects.projects[proj.name]

def test_load_from_path():
	with pytest.raises(FileNotFoundError):
		projects.load_from_path('/tmp/ogn/unexisting/path/')
	with pytest.raises(FileNotFoundError):
		projects.load_from_path(proj_dir+'unexisting_project/')

	os.mkdir('/tmp/ogn/another_dict/')
	projects.save_project_at(model.Project(''), '/tmp/ogn/another_dict/my_project/')
	proj =  projects.load_from_path('/tmp/ogn/another_dict/my_project/')

	assert proj.name == 'my_project'
	assert isinstance(proj, model.Project) 
	assert projects.projects[proj.name]
		
def test_load():
	with pytest.raises(FileNotFoundError):
		projects.load('unexisting_project/')

	projects.save(projects.new('my_project'))
	proj = projects.load('my_project/')

	assert proj.name == 'my_project'
	assert isinstance(proj, model.Project) 
	assert projects.projects[proj.name]

def test_get():
	# never created
	proj = projects.get('proj')

	assert proj.name == 'proj'
	assert isinstance(proj, model.Project) 
	assert proj.name in projects.projects
	
	# alredy stored
	new_proj = projects.new('new_proj')
	proj = projects.get('new_proj')
	assert new_proj is proj

	# alredy saved
	saved_proj = model.Project('saved_proj')
	saved_proj.anims['an_anim'] = model.Anim()
	projects.save(saved_proj)
	proj = projects.get('saved_proj')
	assert 'an_anim' in proj.anims
	assert projects.projects[proj.name]

def test_close():
	projects.get('a_project')
	projects.close('a_project')
	assert 'a_project' not in projects.projects

def test_delete():
	projects.save(projects.get('a_project'))
	projects.close('a_project')
	assert os.path.isdir(proj_dir+'a_project')
	projects.delete('a_project')
	assert not os.path.isdir(proj_dir+'a_project')
