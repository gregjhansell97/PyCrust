from collections import defaultdict

import tie_py._factory
from tie_py._base import TiePyBase
from tie_py._enums import Action

def tie_pyify(obj, owners):
    class_ = obj.__class__
    if class_ in tie_pyify.classes:
        return tie_pyify.classes[class_](obj, owners)

    class TiePyDict(TiePyBase, class_):
        '''
        assumes class_ inherits from dictionary, blends in TiePyBase to create a
        TiePyDict. Monitoring catered to dictionaries
        '''

        '''
        ABSTRACT INHERITED FUNCTIONS
        '''
        def _copy(self, obj):
            for key, value in obj.items():
                self.__setitem__(key, value)
        def _get_steps(self):
            return self.keys()
        def _get_values(self):
            return self.values()


        '''
        MAGIC METHODS
        '''
        def __setitem__(self, key, value):
            '''
            wrapper for set item class, invokes callbacks if needed

            Args:
                key: the key to access the value
                value: the value being assigned
            '''
            if key in self:
                v = self[key]
                if v is value:
                    return class_.__setitem__(self, key, value)
                elif issubclass(v.__class__, TiePyBase):
                    self._remove_paths(key, v)
         
            owners, value = self._tie_pyify(key, value)
            r = class_.__setitem__(self, key, value)
            self._run_callbacks(owners, value, Action.SET) 
            return r

        def __delitem__(self, key):
            v = self[key]
            if issubclass(v.__class__, TiePyBase):
                self._remove_paths(key, v)
            r = class_.__delitem__(self, key)
            self._run_callbacks(self._owners, None, Action.DELETE)
            return r
    tie_pyify.classes[class_] = TiePyDict
    return TiePyDict(obj, owners)

tie_pyify.classes = dict()
