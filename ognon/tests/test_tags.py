from .. import model
from ..tags import tags

def test_loop(cursor):

    assert cursor.element_len(model.Cell(tags=['loop 2'])) == 2
    assert cursor.element_len(model.Cell(tags=['loop 2', 'loop 3'])) == 6
    assert cursor.element_len(model.AnimRef(name='master', tags=['loop 3'])) == 6
    
    anim_ref = model.AnimRef(name='master', tags=['loop 3'])
    cursor.proj.anims['anim_with_tags'] = model.Anim(layers=[model.Layer(elements=[anim_ref])])
    assert cursor.get_element_pos(anim='anim_with_tags', layer=0, frm=4) == (0, anim_ref, 0)

def test_loopfor(cursor):

    assert cursor.element_len(model.Cell(tags=['loopfor 13'])) == 13
    assert cursor.element_len(model.AnimRef(name='master', tags=['loopfor 9'])) == 9
    
    anim_ref = model.AnimRef(name='master', tags=['loopfor 9'])    
    cursor.proj.anims['anim_with_tags'] = model.Anim(layers=[model.Layer(elements=[anim_ref])])
    assert cursor.get_element_pos(anim='anim_with_tags', layer=0, frm=5) == (0, anim_ref, 1)


def test_pendulum(cursor):

    assert cursor.element_len(model.Cell(tags=['pendulum 3'])) == 1
    assert cursor.element_len(model.AnimRef(name='master', tags=['pendulum 2'])) == 3
    
    anim_ref = model.AnimRef(name='master', tags=['pendulum 3'])    
    cursor.proj.anims['anim_with_tags'] = model.Anim(layers=[model.Layer(elements=[anim_ref])])
    assert cursor.get_element_pos(anim='anim_with_tags', layer=0, frm=3) == (0, anim_ref, 1)


def test_pendulum2(cursor):

    assert cursor.element_len(model.Cell(tags=['pendulum2 2'])) == 2
    assert cursor.element_len(model.AnimRef(name='master', tags=['pendulum2 2'])) == 4
    
    anim_ref = model.AnimRef(name='master', tags=['pendulum2 3'])    
    cursor.proj.anims['anim_with_tags'] = model.Anim(layers=[model.Layer(elements=[anim_ref])])
    assert cursor.get_element_pos(anim='anim_with_tags', layer=0, frm=4) == (0, anim_ref, 0)


def test_random(cursor):

    assert cursor.element_len(model.Cell(tags=['random 0'])) == 1
    assert cursor.element_len(model.AnimRef(name='master', tags=['random 0'])) == 2
    

def test_startafter(cursor):

    assert cursor.element_len(model.Cell(tags=['startafter 3'])) == 4
    assert cursor.element_len(model.AnimRef(name='master', tags=['startafter 3'])) == 5
    
    anim_ref = model.AnimRef(name='master', tags=['startafter 3'])    
    cursor.proj.anims['anim_with_tags'] = model.Anim(layers=[model.Layer(elements=[anim_ref])])
    assert cursor.get_element_pos(anim='anim_with_tags', layer=0, frm=4) == (0, anim_ref, 1)

def test_endafter(cursor):

    assert cursor.element_len(model.Cell(tags=['endafter 3'])) == 4
    assert cursor.element_len(model.AnimRef(name='master', tags=['endafter 3'])) == 5
    
    anim_ref = model.AnimRef(name='master', tags=['endafter 3'])    
    cursor.proj.anims['anim_with_tags'] = model.Anim(layers=[model.Layer(elements=[anim_ref])])
    assert cursor.get_element_pos(anim='anim_with_tags', layer=0, frm=2) == (0, anim_ref, 1)
