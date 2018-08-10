import random
#global function call every instance of that object
#function calls on function calls
#
class TiePy:
    __callbacks = []
    __available = []
    def __setattr__(self, name, value):
        prior = None
        if name in self.__dict__:
            prior = self.__dict__[name]
        self.__dict__[name] = value
        for c in self.__callbacks:
            c(name, prior, self.__dict__[name])

    def subscribe(self, callback):
        id_ = len(self.__callbacks)
        if len(self.__available) > 0:
            id_ = self.__available.pop()
        else:
            self.__callbacks.append(None)
        self.__callbacks[id_] = callback
        return id_


    def unsubscribe(self, id_):
        self.__callbacks[id_] =  None
        self.__available.append(id_)
