from ..control import export
import PIL.Image

def test__frm_to_pilimage(cursor):
	assert isinstance(export._frm_to_pilimage(cursor), PIL.Image.Image)
