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

"""
import random

def calculate_len(length, tag_description):
	"""
	Return the length modified by the tag.

	Call the calculate_len function of the tag.
	"""
	tag = tag_description.split()
	tag_name = tag.pop(0)
	if length == 0:
		return 0
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
	if length == 0:
		return 0
	try:
		return tags[tag_name]['calculate_inside_pos'](pos, length, *tag)
	except KeyError:
		return pos

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
}

