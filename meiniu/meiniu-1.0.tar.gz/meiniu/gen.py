import sys


class menupromp(object):
    "Genera menus en base a diccionarios"

    def __init__(self, clase):
        self.promp = "#> "
        self.clase = clase
        self.run = True
        self.excepterror = "Not valid options"
        self.exceptnull = "Not have options"
        self.exceptki = "Goodbye!"

    def banner(self, opciones):
        for x, y in opciones.items():
            print("{}) {}".format(x, y))

    def __dir__(self):
        return [self.clase.__dict__[x] for x in [value for value in self.clase.__dict__ if value[:4] == "opt_"]], [x[4:] for x in [value for value in self.clase.__dict__ if value[:4] == "opt_"]]

    def genfuncs(self):
        return {str(ids+1): value for ids, value in enumerate(self.__dir__()[0])}

    def genmenu(self):
        return {ids+1: value for ids, value in enumerate(self.__dir__()[1])}


def newMenu(obj, intro=""):
    m = menupromp(obj)
    while m.run:
        print(intro)
        m.banner(m.genmenu())
        
        try:
            opt = input("\n"+m.promp)
            m.genfuncs().get(opt)(m)
        #except TypeError:
         #   print(m.excepterror)
        #except ValueError:
         #   print(m.exceptnull)"""
        except KeyboardInterrupt:
            print(m.exceptki)
            sys.exit()

