def move(e, x, y): 
    for l in e.lines:  
        l.coords = [(c+x if not i%2 else c+y) for (i, c) in enumerate(l.coords)]

def xsym(e): 
    for l in e.lines:  
        l.coords = [(0-c+3000 if not i%2 else c) for (i, c) in enumerate(l.coords)]

def ysym(e): 
    for l in e.lines:  
        l.coords = [(0-c+3000 if i%2 else c) for (i, c) in enumerate(l.coords)]

def scale(e, factor): 
    for l in e.lines:  
        l.coords = [int(c*factor) for c in l.coords]