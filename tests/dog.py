from pynoculars import observable

@observable
class Dog:
    '''
    Attributes:

    '''
    YES = 1
    NO = 2
    def __init__(self, name="dogo", age=0):
        self.name = name
        self.age = age
        self.commands = set()
    def bark(self):
        return "wuff"
    def teach(self, cmd:str):
        self.commands.add(cmd.lower())
    def say(self, cmd:str):
        if cmd.lower() in self.commands:
            return Dog.YES
        else:
            return Dog.NO
    def set_name(self, name):
        self._name = name
