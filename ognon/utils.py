"""
This module define utils function.
"""

import configparser

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
	parser.read(path)
	return {k:{k_:convert(v_) for k_, v_ in dict(v).items()}
		for k, v in dict(parser).items()}
