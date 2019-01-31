import threading
import requests
from .. import server

# baseurl = 'http://localhost:40460'
# def test_server():	
# 	thread = threading.Thread(target=server.serve)
# 	thread.start()


# 	requests.get(baseurl+'/index.html')
# 	requests.get(baseurl+'/edit.html')
# 	requests.get(baseurl+'/edito.html')

def test_get_function():
	from ..control.navigator import next_frm
	assert server.get_function("/control/navigator/next_frm") is next_frm
	from ..view import get_lines
	assert server.get_function("/view/get_lines/") is get_lines