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
            self._run_callbacks(self._owners, None, class_.__delitem__)
            return r

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
                self._run_callbacks(owners, self[start:], class_.__iadd__)
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
                distance = len(self)
                for i in range(1, value):
                    for j, v in enumerate(self):
                        self._tie_pytify(j + distance*i, v)
            else:
                return class_.__imul__(self, value)
            r = class_.__imul__(self, value)
            self._run_callbacks(self._owners, self, class_.__imul__)
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
            owners, value = self._tie_pyify(index, value)
            r = class_.__setitem__(self, index, value)
            self._run_callbacks(owners, value, class_.__setitem__)
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
            self._run_callbacks(owners, value, class_.append)
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
            self._run_callbacks(self._owners, self, class_.clear)
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
                self._run_callbacks(owners, self[start:], class_.extend)
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
            owners, value = self._tie_pyify(index, value)
            r = class_.insert(self, index, value)
            self._run_callbacks(owners, value, class_.insert)
            return r


        def remove(self, index):
            '''
            Wrapper for

            Args:
            '''
            pass

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
            self._run_callbacks(self._owners, None, class_.pop)
            return r

        def reverse(self):
            pass



    return TiePyList(obj, owners)
