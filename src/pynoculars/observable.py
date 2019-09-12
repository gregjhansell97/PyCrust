from pynoculars.subscription import Subscription
 

def observable(class_):
    class WrapperClass(class_):
        '''

        Attributes:
            self._callbacks(dict): TODO explanation
        '''
        def __init__(self, *args, **kwargs):
            self._subscribers = dict()
            super(WrapperClass, self).__init__(*args, **kwargs)
        def __getattribute__(self, name: str):
            '''
            called when attribute is accessed; if attribute is a method the 
            overriding behavior is to "decorate" method with _monitor

            Args:
                name(str): name of accessed attribute
            Returns:
                (object): attribute corresponding to name
            '''
            parent = super(WrapperClass, self)
            attr = parent.__getattribute__(name)
            method_type = type(parent.__getattribute__("__init__"))
            if type(attr) == method_type and name != "_monitor":
                return self._monitor(name, attr)
            else:
                return attr
        def __setattr__(self, name: str, value):
            '''
            called when setting an attribute; invokes callbacks if attribute
            has registered callbacks

            Args:
                name(str): name of accessed attriubte
                value(object): new value for attribute corresponding to name
            '''
            parent = super(WrapperClass, self)
            try:
                old_value = parent.__getattribute__(name)
            except AttributeError:
                old_value = None
            parent.__setattr__(name, value)
            if name not in self._subscribers:
                self._subscribers[name] = []
            for s in self._subscribers[name]:
                s.callback(self, old_value, value)
        def _monitor(self, name: str, method):
            '''
            decorator that monitors when a function/method is invoked and
            invokes callbacks related to the method
            '''
            def wrapper_function(*args, **kwargs):
                retval = method(*args, **kwargs)
                if name not in self._subscribers:
                    self._subscribers[name] = []
                for s in self._subscribers[name]:
                    s.callback(self, retval, *args, **kwargs)
                return retval
            return wrapper_function
        def subscribe(self, name: str, callback):
            '''
            registers a callback to a specified attribute name (when it gets
            called)

            Args:
                name(str): name of attribute, can refer to both a method or
                    object instance
            '''
            
            # throw if not an attribute
            parent = super(WrapperClass, self)
            try:
                parent.__getattribute__(name)
            except AttributeError:
                raise AttributeError
            sub = Subscription(self, name, callback)
            if name not in self._subscribers:
                self._subscribers[name] = []
            self._subscribers[name].append(sub)
            return sub
    return WrapperClass 
