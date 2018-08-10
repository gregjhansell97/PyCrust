from TiePy import TiePy

class Greg(TiePy):
    def __init__(self):
        self.x = 10

def variable_changed(name, prior, current):
    print((name, prior, current))



if __name__ == "__main__":
    g = Greg()
    g.x = 98
    id_ = g.subscribe(variable_changed)
    print(id_)
    g.x = 69
