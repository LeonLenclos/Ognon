"""
This module define tags function.
"""

def calculate_len(length, tag_description):
	"""
	Return the length modified by the tag.

	Call the calculate_len function of the tag.
	"""
	tag = tag_description.split()
	tag_name = tag.pop(0)
	try:
		return tags[tag_name]['calculate_len'](length, *tag)
	except KeyError:
		return length

def calculate_inside_pos(pos, length, tag_description):
	"""
	Return the inside position modified by the tag.

	Call the calculate_inside_pos function of the tag.
	"""
	tag = tag_description.split()
	tag_name = tag.pop(0)
	try:
		return tags[tag_name]['calculate_inside_pos'](pos, length, *tag)
	except KeyError:
		return pos

tags = {
	'loop':{
		'calculate_len':lambda length, n: int(n)*length,
		'calculate_inside_pos':lambda pos, length, n: pos%length,
	},
}