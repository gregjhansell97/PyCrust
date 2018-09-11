from TiePy import TiePyify

#this file uses an example

class Greg:
    def __init__(self):
        self.x = {
            "test": 98
        }

    def k(self):
        print("hello world")

class Gerg:
    def __init__(self):
        self.x = 98

def dur():
    print("durr")

def variable_changed(name, prior, current):
    print((name, prior, current))

if __name__ == "__main__":
    # g = Gerg()
    # g.x = 75
    # id_ = g.subscribe(variable_changed)
    # g.x = 565600
    g = TiePyify(Greg())
    g.x["test"] = 98
    id_ = g.subscribe(variable_changed)
    print(id_)
    g.x["test"] = 70
    g.__dict__["k"] = d
    print("Hello world")
