from .. import model
from ..tags import tags

def test_loop(cursor):

	assert cursor.element_len(model.Cell(tags=['loop 2'])) == 2
	assert cursor.element_len(model.Cell(tags=['loop 2', 'loop 3'])) == 6
	assert cursor.element_len(model.AnimRef(name='master', tags=['loop 3'])) == 6
	anim_ref = model.AnimRef(name='master', tags=['loop 3'])
	cursor.proj.anims['anim_with_tags'] = model.Anim(layers=[model.Layer(elements=[anim_ref])])
	assert cursor.get_element_pos(anim='anim_with_tags', layer=0, frm=4) == (0, anim_ref, 0)

