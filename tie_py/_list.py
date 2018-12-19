import tie_py._factory

from tie_py._base import TiePyBase
from tie_py._enums import Action

def tie_pyify(obj, callbacks={}):
    class_ = obj.__class__
    class TiePyList(TiePyBase, class_):
        '''
        assumes class_ inherits from dictionary, blends in TiePyBase to create a
        TiePyList. Monitoring catered to lists
        '''

        '''
        ABSTRACT INHERITED FUNCTIONS
        '''

        def __iadd__(self, iterable):
            '''
            Wrapper for

            Args:
            '''
            start = len(self)
            tie_pyified_iterable = map(lambda iv: self._convert(iv[1], start + iv[0]), enumerate(iterable))
            r = class_.__iadd__(self, tie_pyified_iterable)
            self._run_callbacks(start, self[start:], Action.EXTEND)
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
            if 0 <= index < len(self) and self[index] is value:
                return class_.__setitem__(self, index, value)
            value = self._convert(value, index)
            r = class_.__setitem__(self, index, value)
            self._run_callbacks(index, value, Action.SET)
            return r

        def _convert(self, value, step):
            '''
            '''
            if value not in self._chain and value is not self:
                callbacks = {}
                for id_ in self._callbacks.keys():
                    owner, path, cb = self._callbacks[id_]
                    callbacks[id_] = (owner, path + [step], cb)
                return tie_py._factory.tie_pyify(value, callbacks=callbacks)
            return value

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
            value = self._convert(value, step)
            r = class_.append(self, value)
            self._run_callbacks(step, value, Action.SET)
            return r

        def clear(self):
            '''
            Wrapper for

            Args:
            '''
            r = class_.clear(self)
            self._run_callbacks(0, self, Action.CLEAR)


        def extend(self, iterable):
            '''
            Wrapper for
 
            Args:
            '''
            start = len(self)
            tie_pyified_iterable = map(lambda iv: self._convert(iv[1], start + iv[0]), enumerate(iterable))
            r = class_.extend(self, tie_pyified_iterable)
            self._run_callbacks(start, self[start:], Action.EXTEND)
            return r

        def insert(self, index, value):
            '''
            Wrapper for

            Args:
            '''
            value = self._convert(value)
            r = class_.insert(self, index, value)
            self._run_callbacks(index, self[index:], Action.EXTEND) 
            return r 


        def remove(self, index):
            '''
            Wrapper for

            Args:
            '''
            pass


    return TiePyList(obj, callbacks=callbacks)
