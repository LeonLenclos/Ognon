from ..control import exporter
import PIL.Image

def test__frm_to_pilimage(cursor):
	assert isinstance(exporter._frm_to_pilimage(cursor), PIL.Image.Image)
