from .. import model

def test_model():
	p = model.Project('testing-project')

	assert p.name == 'testing-project'
	assert 'master' in p.anims
	assert type(p.anims['master']) is model.Anim
	assert type(p.anims['master'].layers[0]) is model.Layer
	assert type(p.anims['master'].layers[0].elements[0]) is model.Cell
	assert model.Line([0,1,2,3]).coords == [0,1,2,3]