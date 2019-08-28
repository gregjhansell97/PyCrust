
def _monitor(instance_, method):
     def wrapper_function(*args, **kwargs):
         print("pre")
         retval = method(*args, **kwargs)
         print("post")
         return retval
     return wrapper_function


def observable(class_):
    class WrapperClass(class_):
        def __init__(self, *args, **kwargs):
            super(WrapperClass, self).__init__(*args, **kwargs)
        def __getattribute__(self, attr_name: str):
            '''
            called when attribute of class_ is accessed
            '''
            parent = super(WrapperClass, self)
            attr = parent.__getattribute__(attr_name)
            if type(attr) == type(parent.__init__):
                return _monitor(self, attr)
            else:
                return attr
        def subscribe(self, method, callback):
            print("subscribing")
    return WrapperClass
     
           
