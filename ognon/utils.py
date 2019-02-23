"""
This module define utils function.
"""

import configparser
import os

def pkgabspath(file=''):
	"""
	Return the absolute path of a given file in the current package 
	"""
	return os.path.join(os.path.dirname(__file__), file)

def parse_config(path):
	"""
	Return a the given config file as a dict of dicts.

	Values are converted into int, float, bool or string.
	"""
	def convert(value):
		try: return int(value)
		except ValueError:
			try: return float(value)
			except ValueError:
				if value == 'true': return True
				if value == 'false': return False
				else : return value
	parser = configparser.ConfigParser()
	with open(path) as f:
		parser.read_file(f)
	return {k:{k_:convert(v_) for k_, v_ in dict(v).items()}
		for k, v in dict(parser).items()}
