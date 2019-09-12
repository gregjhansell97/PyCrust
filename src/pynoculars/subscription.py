import weakref

class Subscription:
    '''
    '''
    def __init__(self, observed_instance, name, callback):
        self._observed_weak_ref = weakref.ref(observed_instance) 
        self.name = name
        self.callback = callback
    def unsubscribe(self):
        instance = self._observed_weak_ref()
        if instance is None:
            raise ReferenceError
        instance._subscribers[self.name].remove(self)
