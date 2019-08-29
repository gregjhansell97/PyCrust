
def _monitor(instance, method):
     def wrapper_function(*args, **kwargs):
         retval = method(*args, **kwargs)
         for cb in instance.callbacks:
             cb(instance, retval, *args, **kwargs)
         return retval
     return wrapper_function


def observable(class_):
    class WrapperClass(class_):
        '''

        Attributes:
            self._callbacks(dict): TODO explanation
        '''
        def __init__(self, *args, **kwargs):
            self._callbacks = dict()
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
            if type(attr) == method_type:
                return _monitor(self, attr)
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
            parent.__setattr__(name, value)
            for cb in self._callbacks:
                cb(self, name, value)
        def subscribe(self, name: str, callback):
            '''
            registers a callback to a specified attribute name (when it gets
            called)

            Args:
                name(str): name of attribute, can refer to both a method or
                    object instance
            '''
            if name not in self._callbacks:
                self._callbacks[name] = []
            self._callbacks[name].append(callback)
    return WrapperClass
     
           
