import pytest
from ..	cursor import Cursor
from .. import model
from .. import control
import os



@pytest.fixture
def cursor():
	"""
	Create a cursor object pointing to a project object as
	
	Project : 'testing-project'
	  Anim : 'master'
	    Layer : 0
		  Element : 0 -> Cell
		  Element : 1 -> Cell
		Layer : 1
		  Element : 0 -> Cell
	  Anim : 'testing-anim'
		Layer : 0
		  Element : 0 -> Cell
	  Anim : 'testing-anim-with-animref'
		Layer : 0
		  Element : 1 -> Cell
		  Element : 0 -> AnimRef('master')
	"""  
	proj = model.Project('testing')
	proj.anims['master'].layers.append(model.Layer())
	proj.anims['master'].layers[0].elements.append(model.Cell())
	proj.anims['testing-anim'] = model.Anim()
	proj.anims['testing-anim-with-animref'] = model.Anim()
	proj.anims['testing-anim-with-animref'].layers[0].elements.append(model.AnimRef('master'))

	c = Cursor(proj)
	c.loop = False
	return c