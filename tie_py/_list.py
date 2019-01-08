import tie_py._factory

from itertools import tee
from tie_py._base import TiePyBase
from tie_py._enums import Action

def tie_pyify(obj, owners):
    class_ = obj.__class__
    class TiePyList(TiePyBase, class_):
        '''
        assumes class_ inherits from dictionary, blends in TiePyBase to create a
        TiePyList. Monitoring catered to lists
        '''

        '''
        ABSTRACT INHERITED FUNCTIONS
        '''

        def __iadd__(self, itr):
            '''
            Wrapper for

            Args:
            '''
            #same as extend code
            start = len(self)
            tp_itr_2, tp_itr_1  = tee(map(
                lambda iv: self._tie_pyify(start + iv[0], iv[1]), enumerate(itr)
            ))
            values = map(lambda owner_value: owner_value[1], tp_itr_1)
            r = class_.__iadd__(self, values)

            try:
                owners, value = next(tp_itr_2)
            except StopIteration: 
                pass
            else:
                self._run_callbacks(owners, self[start:], Action.EXTEND)
            return r

        def __imul__(self, v):
            '''
            Wrapper for

            Args:
            '''
            pass

        def __setitem__(self, index, value):
            '''
            Wrapper for
  
            Args:
            '''
            owner = None
            if index in range(len(self)):
                v = self[index]
                if v is value:
                    return class_.__setitem__(self, index, value)
                elif issubclass(v.__class__, TiePyBase):
                    self._remove_paths(index, v)
                owners, value = self._tie_pyify(index, value)
            r = class_.__setitem__(self, index, value)
            self._run_callbacks(owners, value, Action.SET)
            return r

        def _copy(self, obj):
            '''
            '''
            self.extend(obj)

        def _get_steps(self):
            '''
            '''
            return range(len(self))

        def _get_values(self):
            '''
            '''
            return self.__iter__()

        def append(self, value):
            '''
            Wrapper for
       
            Args:
            '''
            step = len(self)
            owners, value = self._tie_pyify(step, value)
            r = class_.append(self, value)
            self._run_callbacks(owners, value, Action.SET)
            return r

        def clear(self):
            '''
            Wrapper for

            Args:
            '''
            for i, v in enumerate(self):
                if issubclass(v.__class__, TiePyBase):
                    self._remove_paths(i, v)
            r = class_.clear(self)
            self._run_callbacks(self._owners, self, Action.CLEAR)
            return r


        def extend(self, itr):
            '''
            Wrapper for
 
            Args:
            '''
            #same code as extend
            start = len(self)
            tp_itr_2, tp_itr_1  = tee(map(
                lambda iv: self._tie_pyify(start + iv[0], iv[1]), enumerate(itr)
            ))
            values = map(lambda owner_value: owner_value[1], tp_itr_1)
            r = class_.extend(self, values)

            try:
                owners, value = next(tp_itr_2)
            except StopIteration: 
                pass
            else:
                self._run_callbacks(owners, self[start:], Action.EXTEND)
            return r

        def insert(self, index, value):
            '''
            Wrapper for

            Args:
            '''
            pass


        def remove(self, index):
            '''
            Wrapper for

            Args:
            '''
            pass


    return TiePyList(obj, owners)
