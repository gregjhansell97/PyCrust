import tie_py._dict
import tie_py._list
#import tie_py._set
from tie_py._base import TiePyBase

def tie_pyify(obj, callbacks={}):
    '''
    recursive factory function that decorates an object

    Args:
        obj (obj): the object to be decorated with TiePyBase functionality
        callbacks (dict): dictionary of callbacks (notionally used for objects
        that are already instances of TiePyBase and just need callbacks injected

    Returns:
        (TiePyBase): a wrapped copy of obj that exhibits the behaviors of
            TiePyBase
    '''
    if issubclass(obj.__class__, TiePyBase):
        #subclass of TiePyBase, inject callbacks into it
        obj._extend_callbacks(callbacks)
        return obj
    elif "__dict__" in dir(obj):
        #has custom class_attributes
        raise ValueError("Not on custom classes just yet")
        obj.__dict__ = tie_py.dict.tie_pyify(obj.__dict__, callbacks)
        return obj #same object, different dict
    elif issubclass(obj.__class__, dict):
        #dictionaries
        return tie_py._dict.tie_pyify(obj, callbacks)
    elif issubclass(obj.__class__, list):
        #lists
        return tie_py._list.tie_pyify(obj, callbacks)
    elif False: #issubclass(obj.__class__, set):
        #sets
        return tie_py._set.tie_pyify(obj, callbacks)
    else:
        #is probably a built-in object
        return obj
