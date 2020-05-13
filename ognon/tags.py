"""
This module define tags function.

Tags defined here :

- `loop n`
- `loopfor n`
- `pendulum n`
- `pendulum2 n`
- `random n`
- `startafter n`
- `endafter n`
- `draft`
- `mask`
"""
import random


def read_tag_description(tag_description):
	"""
	Return a two elements tuple with tag name and tag args.
	"""
	splited = tag_description.split()
	return splited.pop(0), splited

def calculate_len(length, tag_description):
	"""
	Return the length modified by the tag.

	Call the calculate_len function of the tag.
	"""
	tag_name, args = read_tag_description(tag_description)

	if length == 0:
		return 0
	try:
		return tags[tag_name]['calculate_len'](length, *args)
	except KeyError:
		return length

def calculate_inside_pos(pos, length, tag_description):
	"""
	Return the inside position modified by the tag.

	Call the calculate_inside_pos function of the tag.
	"""
	tag_name, args = read_tag_description(tag_description)

	if length == 0:
		return 0
	try:
		return tags[tag_name]['calculate_inside_pos'](pos, length, *args)
	except KeyError:
		return pos

def calculate_coords(coords, playing, pos, length, tag_description):
	"""
	Return the lines description modified by the tag.

	Call the calculate_lines function of the tag.
	"""
	tag_name, args = read_tag_description(tag_description)

	try:
		return tags[tag_name]['calculate_coords'](coords, playing, pos, length, *args)
	except KeyError:
		return coords

def calculate_line_type(line_type, playing, tag_description):
	"""
	Return the lines description modified by the tag.

	Call the calculate_lines function of the tag.
	"""
	tag_name, args = read_tag_description(tag_description)

	try:
		return tags[tag_name]['calculate_line_type'](line_type, playing, *args)
	except KeyError:
		return line_type


def random_calculate_inside_pos(pos, length, n):
	random.seed(pos+int(n))
	return random.randint(0,length-1)

tags = {
	'loop':{
		'calculate_len':lambda length, n: int(n)*length,
		'calculate_inside_pos':lambda pos, length, n: pos%length,
	},
	'loopfor':{
		'calculate_len':lambda length, n: int(n),
		'calculate_inside_pos':lambda pos, length, n: pos%length,
	},
	'pendulum':{
		'calculate_len':lambda length, n: length + (int(n)-1)*(length-1),
		'calculate_inside_pos':lambda pos, length, n:\
			pos%(2*(length-1))\
			if pos%(2*(length-1)) < length\
			else 2*(length-1) - pos%(2*(length-1))
	},
	'pendulum2':{
		'calculate_len':lambda length, n: int(n)*length,
		'calculate_inside_pos':lambda pos, length, n:\
			pos%(2*length)\
			if pos%(2*length) < length\
			else 2*length - pos%(2*length) - 1
	},
	'random':{
		'calculate_len':lambda length, n: length,
		'calculate_inside_pos': random_calculate_inside_pos
	},
	'startafter':{
		'calculate_len':lambda length, n: length + int(n),
		'calculate_inside_pos':lambda pos, length, n: 0 if pos < length-1 else pos - int(n)
	},
	'endafter':{
		'calculate_len':lambda length, n: length + int(n),
		'calculate_inside_pos':lambda pos, length, n: pos if pos < length-1 else length-1
	},
	'draft':{
		'calculate_line_type':lambda line_type, playing: line_type if playing else line_type.union({'draft'}),
		'calculate_coords':lambda coords, playing, pos, length: [] if playing else coords
	},
	'mask':{
		'calculate_line_type':lambda line_type, playing: line_type.union({'mask'})
	},
}

