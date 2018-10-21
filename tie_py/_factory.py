import tie_py._dict
import tie_py._list
#import tie_py._set
from tie_py._base import TiePyBase

def tie_pyify(obj, callbacks={}):
    if issubclass(obj.__class__, TiePyBase):
        obj._extend_callbacks(callbacks)
        return obj
    elif "__dict__" in dir(obj): #has class_attributes
        raise ValueError("Not on custom classes just yet")
        obj.__dict__ = tie_py.dict.tie_pyify(obj.__dict__, callbacks)
        return obj #same object, different dict
    elif issubclass(obj.__class__, dict):
        return tie_py._dict.tie_pyify(obj, callbacks)
    elif issubclass(obj.__class__, list):
        return tie_py._list.tie_pyify(obj, callbacks)
    elif False: #issubclass(obj.__class__, set):
        return tie_py._set.tie_pyify(obj, callbacks)
    else:
        return obj
