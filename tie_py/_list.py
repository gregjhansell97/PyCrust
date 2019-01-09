import tie_py._factory

from itertools import tee
from tie_py._base import TiePyBase

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

        def __delitem__(self, index):
            index = index if index >= 0 else index + len(self)
            if index not in range(len(self)):
                return class_.__delitem__(self, index)
            values = self[index:] #values to the right of index affected
            for i, v in enumerate(values):
                if issubclass(v.__class__, TiePyBase):
                    self._remove_paths(index + i, v) #must remove current index
                    if i > 0: #add new index path if not the item being deleted
                        self._tie_pyify(index + i - 1, v)
            r = class_.__delitem__(self, index)
            self._run_callbacks(class_.__delitem__, (self, index))
            return r

        def __iadd__(self, itr):
            '''
            Wrapper for

            Args:
            '''
            #same as extend code
            start = len(self)
            tp_itr  = map(
                lambda iv: self._tie_pyify(start + iv[0], iv[1]), enumerate(itr)
            )

            r = class_.__iadd__(self, tp_itr)
            self._run_callbacks(class_.__iadd__,  (self, self[start:]))
            return r

        def __imul__(self, value):
 
            '''
            Wrapper for

            Args:
            '''  
            if value < 1: # same idea as clear
                for i, v in enumerate(self):
                    if issubclass(v.__class__, TiePyBase):
                        self._remove_paths(i, v)
            elif value > 1: #gotta add new paths
                length = len(self)
                for i in range(1, value):
                    for j, v in enumerate(self):
                        self._tie_pyify(j + length*i, v)
            else:
                return class_.__imul__(self, value)
            r = class_.__imul__(self, value)
            self._run_callbacks(class_.__imul__, (self, value))
            return r

        def __setitem__(self, index, value):
            '''
            Wrapper for
  
            Args:
            '''
            index = index if index >= 0 else index + len(self)
            if index not in range(len(self)):
                return class_.__setitem__(self, index)

            v = self[index]
            if v is value:
                return class_.__setitem__(self, index, value)
            elif issubclass(v.__class__, TiePyBase):
                self._remove_paths(index, v)
            value = self._tie_pyify(index, value)
            r = class_.__setitem__(self, index, value)
            self._run_callbacks(class_.__setitem__, (self, index, value))
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
            value = self._tie_pyify(step, value)
            r = class_.append(self, value)
            self._run_callbacks(class_.append, (self, value))
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
            self._run_callbacks(class_.clear, (self,))
            return r


        def extend(self, itr):
            '''
            Wrapper for
 
            Args:
            '''
            start = len(self)
            tp_itr  = map(
                lambda iv: self._tie_pyify(start + iv[0], iv[1]), enumerate(itr)
            )
            r = class_.extend(self, tp_itr)

            self._run_callbacks(class_.extend, (self, self[start:]))
            return r

        def insert(self, index, value):
            '''
            Wrapper for

            Args:
            '''
            index = index if index >= 0 else index + len(self)
            
            #keeps the insert in range
            if index > len(self): index = len(self)
            elif index < 0: index = 0
            
            values = self[index:] #values to the right of index affected
            for i, v in enumerate(values):
                if issubclass(v.__class__, TiePyBase):
                    self._remove_paths(index + i, v) #must remove current index path
                    self._tie_pyify(index + i + 1, v)
                
            #now we need to set the item so to speak
            value = self._tie_pyify(index, value)
            r = class_.insert(self, index, value)
            self._run_callbacks(class_.insert, (self, index, value))
            return r


        def remove(self, value):
            '''
            Wrapper for

            Args:
            '''
            val_detected = False
            for i, v in enumerate(self):
                if val_detected:
                    if issubclass(v.__class__, TiePyBase):
                        self._remove_paths(i, v)
                        self._tie_pyify(i - 1, v) 
                elif value == v:
                    val_detected = True

            r = class_.remove(self, value)
            self._run_callbacks(class_.remove, (self, value))
            return r
 
            

        def pop(self, index=-1):
            index = index if index >= 0 else index + len(self)
            if index not in range(len(self)):
                return class_.pop(self, index)
            values = self[index:] #values to the right of index affected
            for i, v in enumerate(values):
                if issubclass(v.__class__, TiePyBase):
                    self._remove_paths(index + i, v) #must remove current index
                    if i > 0: #add new index path if not the item being deleted
                        self._tie_pyify(index + i - 1, v)
            r = class_.pop(self, index)
            self._run_callbacks(class_.pop, (self, index))
            return r

        def reverse(self):
            max_index = len(self) - 1
            for i, v in enumerate(self):
                if issubclass(v.__class__, TiePyBase):
                    self._remove_paths(i, v)
                    self._tie_pyify(max_index - i)
            r = class_.reverse(self)
            self._run_callbacks(class_.reverse, (self,))
            return r

    return TiePyList(obj, owners)
