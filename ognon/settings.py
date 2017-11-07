from tkinter import *


class Settings():
    """docstring for Settings"""
    def __init__(self):
        self.settings = dict()

    def __iter__(self):
        return iter(self.settings)

    def __getitem__(self, k):
        return self.settings[k].value

    def __setitem__(self, k, v):
        self.settings[k].value = v

    def option(self, name, value, desc):
        self.settings[name] = Option(name, value, desc)

    def edit(self):
        win = Tk()
        win.geometry("{}x{}".format(200, 400))
        win.resizable(width=False, height=True)

        text = Text(master=win, background='PeachPuff1')
        text.pack(side=TOP, fill=BOTH)
        text.insert(END, self.to_text())
        Button(win, text='Close', command=win.destroy).pack(side=LEFT)
        Button(win, text='Save', command=lambda: self.from_text(text.get('0.0', END))).pack(side=LEFT)

    def to_text(self):
        txt = ""
        first_line = True
        for k in self:
            if first_line:
                first_line = False
            else:
                txt += "\n"
            txt += "{} : {}".format(k, self[k])
        return txt

    def from_text(self, txt):
        lines = txt.split("\n")
        for l in lines:
            if ':' in l:
                option_name = l.split(":")[0].strip()
                option_value = l.split(":")[1].strip()
                print(self[option_name], option_name)
                if option_value == 'True':
                    self[option_name] = True
                elif option_value == 'False':
                    self[option_name] = False
                elif option_value.isdigit():
                    self[option_name] = int(option_value)


class Option():
    """an option to set with settings"""
    def __init__(self, name, value, desc):
        self.name = name
        self.value = value
        self.desc = desc


settings = Settings()

settings.option("onion skinning show", True, "")
settings.option("onion skinning loop", True, "")
settings.option("onion skinning range", 1, "")
settings.option("play in loop", True, "")
settings.option("play speed", 12, "images per seconds")
settings.option("pen width", 2, "px")
settings.option("zoom", 100, "%")
settings.option('export scale', 2, "multiplier")
