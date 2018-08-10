
class TiePy:
    '''
    Provides call back solutions for field variables and functions that need to be monitored by other objects

    Attributes:
        __callbacks (list): list of callbacks that get called on state change
        __available (list): list of id's up for grabs

    '''

    #used as instance variables in inherited class
    __callbacks = []
    __available = []
    def __setattr__(self, name, value):
        '''
        overridden magic method that is called when an attribute is set. Care is
        needed when overriding this class in children

        Args:
            name: the field variable begin assigned to
            value: the value being assigned
        '''
        prior = None
        if name in self.__dict__:
            prior = self.__dict__[name]
        self.__dict__[name] = value
        #goes through callbacks
        for c in self.__callbacks:
            if c is not None: #checks to make sure id is not none
                c(name, prior, self.__dict__[name])

    def subscribe(self, callback):
        '''
        on state variable change, callback submitted is called

        Args:
            callback (function(name, prior, current)): The function that gets
                called when a field variable changes

        Returns:
            int: the id of the subscriber
        '''
        id_ = len(self.__callbacks)
        if len(self.__available) > 0:
            id_ = self.__available.pop()
        else:
            self.__callbacks.append(None)
        self.__callbacks[id_] = callback
        return id_


    def unsubscribe(self, id_):
        '''
        removes the callback function with that id_ from the subscription list

        Args:
            id_: the id of the subscriber
        '''
        self.__callbacks[id_] =  None
        self.__available.append(id_)
