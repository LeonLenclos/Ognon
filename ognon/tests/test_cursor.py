import pytest
from .. import model

def test_get_pos(cursor):
    # test that it always return _pos values
    for k in ('anim', 'layer', 'frm'):
        assert cursor.get_pos(k) == cursor.get_pos()[k] == cursor._pos[k]

    # test that it always return existing objects
    cursor._pos = {'anim':'unexisting-project','layer':9999,'frm':9999}
    assert (cursor.get_pos('anim') in cursor.proj.anims)
    assert cursor.get_pos('layer') < len(cursor.proj.anims[cursor.get_pos('anim')].layers)
    assert cursor.get_pos('frm') < cursor.anim_len()

def test_set_pos(cursor):

    # test set_pos on anim
    assert cursor.get_pos('anim') == 'master'
    cursor.set_pos(anim='testing-anim')
    assert cursor.get_pos('anim') == 'testing-anim'
    cursor.set_pos(anim='unexisting-anim')
    assert cursor.get_pos('anim') == 'master'

    # test set_pos on layer
    assert cursor.get_pos('layer') == 0
    cursor.set_pos(layer=1)
    assert cursor.get_pos('layer') == 1
    cursor.set_pos(layer=-10)
    assert cursor.get_pos('layer') == 0
    cursor.set_pos(layer=10)
    assert cursor.get_pos('layer') == 0

    # test set_pos on frm
    assert cursor.get_pos('frm') == 0
    cursor.set_pos(anim='master', layer=0, frm=1)
    assert cursor.get_pos('frm') == 1
    cursor.proj.config['play']['loop'] = True
    cursor.set_pos(anim='master', layer=0, frm=2)
    assert cursor.get_pos('frm') == 0
    cursor.set_pos(anim='master', layer=0, frm=-1)
    assert cursor.get_pos('frm') == 1
    cursor.proj.config['play']['loop'] = False
    cursor.set_pos(anim='master', layer=0, frm=10)
    assert cursor.get_pos('frm') == 1
    cursor.set_pos(anim='master', layer=0, frm=-10)
    assert cursor.get_pos('frm') == 0

def test_constrain_frm(cursor):
    cursor.proj.config['play']['loop'] = False
    assert cursor.constrain_frm(10) == 1
    assert cursor.constrain_frm(1) == 1
    assert cursor.constrain_frm(-10) == 0
    assert cursor.constrain_frm(0) == 0
    cursor.proj.config['play']['loop'] = True
    assert cursor.constrain_frm(-2) == 0 
    assert cursor.constrain_frm(-1) == 1 
    assert cursor.constrain_frm(0) == 0 
    assert cursor.constrain_frm(1) == 1 
    assert cursor.constrain_frm(2) == 0 
    assert cursor.constrain_frm(3) == 1 

def test_get_anim(cursor):
    assert cursor.get_anim() is cursor.proj.anims['master']
    assert cursor.get_anim('testing-anim') is cursor.proj.anims['testing-anim']
    with pytest.raises(KeyError):
        cursor.get_anim('unexisting-anim')

def test_get_layer(cursor):
    assert cursor.get_layer() is cursor.proj.anims['master'].layers[0]
    assert cursor.get_layer(anim='testing-anim') is cursor.proj.anims['testing-anim'].layers[0]
    assert cursor.get_layer(layer=1) is cursor.proj.anims['master'].layers[1]
    with pytest.raises(IndexError):
        cursor.get_layer(layer=10)

def test_get_element_pos(cursor):
    assert cursor.get_element_pos() == (0, cursor.proj.anims['master'].layers[0].elements[0], 0)
    assert cursor.get_element_pos(layer=1) == (0, cursor.proj.anims['master'].layers[1].elements[0], 0)
    assert cursor.get_element_pos(frm=1) == (1, cursor.proj.anims['master'].layers[0].elements[1], 0)
    assert cursor.get_element_pos(anim='testing-anim-with-animref', frm=5) == (1, cursor.proj.anims['testing-anim-with-animref'].layers[0].elements[1], 4)

def test_anim_len(cursor):
    assert cursor.anim_len() == 2
    assert cursor.anim_len('testing-anim') == 1
    assert cursor.anim_len('master') == 2
    assert cursor.anim_len('testing-anim-with-animref') == 8

def test_element_len(cursor):
    assert cursor.element_len(cursor.get_element()) == 1
    assert cursor.element_len(model.Cell()) == 1
    assert cursor.element_len(model.AnimRef('master')) == 2
