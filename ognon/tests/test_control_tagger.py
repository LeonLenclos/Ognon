from ..control import tagger


def test_add_tag(cursor):
	assert tagger.add_tag(cursor, 'loop 3') is None
	assert 'loop 3' in cursor.get_element().tags

def test_replace_tag(cursor):
	tagger.add_tag(cursor, 'loop 3')
	assert tagger.replace_tag(cursor, 'loop 4', 0) is None
	assert 'loop 4' in cursor.get_element().tags
	assert 'loop 3' not in cursor.get_element().tags

def test_rm_tag(cursor):
	tagger.add_tag(cursor, 'loop 3')
	assert tagger.rm_tag(cursor, 0) is None
	assert 'loop 3' not in cursor.get_element().tags

def test_rm_tags(cursor):
	tagger.add_tag(cursor, 'loop 3')
	tagger.add_tag(cursor, 'loop 4')
	assert tagger.rm_tags(cursor) is None
	assert len(cursor.get_element().tags) == 0
