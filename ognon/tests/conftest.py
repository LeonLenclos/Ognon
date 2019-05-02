import pytest
from ..cursor import Cursor
from .. import model
from .. import view
from .. import control
import os, shutil

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
        Layer : 2
          Element : 0 -> Cell
      Anim : 'testing-anim'
        Layer : 0
          Element : 0 -> Cell
      Anim : 'testing-anim-with-animref'
        Layer : 0
          Element : 0 -> Cell
          Element : 1 -> AnimRef('long-anim')
      Anim : 'long-anim'
        Layer : 0
          Element : 0 -> Cell
          Element : 1 -> Cell
          Element : 2 -> Cell
          Element : 3 -> Cell
          Element : 4 -> Cell
          Element : 5 -> Cell
          Element : 6 -> Cell
      Anim : 'testing-anim-with-self-ref'
        Layer : 0
          Element : 0 -> Cell
          Element : 1 -> AnimRef('anim-with-self-ref')
      Anim : 'testing-anim-with-unexisting-ref'
        Layer : 0
          Element : 0 -> AnimRef('unexisting-anim')
      Anim : 'testing-layers'
        Layer : 0
          Element : 0 -> Cell
        Layer : 1
          Element : 0 -> Cell
        Layer : 2
          Element : 0 -> Cell
      Anim : 'empty-anim'
        Layer : 0
      Anim : 'really-empty-anim'
    """  

    proj = model.Project(
      name='testing',
      anims={
        'master':model.Anim(layers=[
            model.Layer(elements=[model.Cell(), model.Cell()]),
            model.Layer(elements=[model.Cell()]),
          ]),
        'testing-anim':model.Anim(layers=[
            model.Layer(elements=[model.Cell()]),
          ]),
        'testing-anim-with-animref':model.Anim(layers=[
            model.Layer(elements=[model.Cell(),model.AnimRef('long-anim')]),
          ]),
        'long-anim':model.Anim(layers=[
            model.Layer(elements=[model.Cell() for _ in range(7)]),
          ]),
        'testing-anim-with-self-ref':model.Anim(layers=[
            model.Layer(elements=[model.Cell(), model.AnimRef('testing-anim-with-self-ref')]),
          ]),
        'testing-anim-with-unexisting-ref':model.Anim(layers=[
            model.Layer(elements=[model.AnimRef('unexisting-anim')]),
          ]),
        'testing-layers':model.Anim(layers=[
            model.Layer(elements=[model.Cell()]),
            model.Layer(elements=[model.Cell()]),
            model.Layer(elements=[model.Cell()]),
        ]),
        'empty-anim':model.Anim(layers=[
            model.Layer(elements=[])
        ]),
        'really-empty-anim':model.Anim(layers=[]),

      }
      )
    c = Cursor(proj)
    c.proj.config['play']['loop'] = False
    return c


def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    if os.path.isdir('/tmp/ogn/'):
        shutil.rmtree('/tmp/ogn/')
