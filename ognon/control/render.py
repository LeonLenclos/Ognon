
class Render():
    """Allow to navigate into one Animation."""
    def __init__(self, ognproject):
        self.ognproject = ognproject

    def get_lines(self, cursor):
    	lines=[]
    	for frm in cursor.get_frms():
    		if frm:
    			for line in frm.lines:
    				lines.append(line.get_data())
    	return lines