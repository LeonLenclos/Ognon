from .. import utils

test_ini = """
;comment

[sectionA]
optionA = 1
optionB = .5
optionC = true
optionD = false
optionE = #ffffff
optionF = foo

[sectionB]
option = Bar
"""
def test_parse_config():
	with open('/tmp/ogn/test.ini', 'w') as f:
		f.write(test_ini)
	assert utils.parse_config('/tmp/ogn/test.ini') == {
	'sectionA':{
		'optiona':1,
		'optionb':.5,
		'optionc':True,
		'optiond':False,
		'optione':'#ffffff',
		'optionf':'foo',
	},'sectionB':{
		'option':'Bar'
	},'DEFAULT':{}
}
