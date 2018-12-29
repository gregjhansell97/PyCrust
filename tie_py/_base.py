from itertools import zip_longest
from tie_py._enums import Action

def get_id():
    if len(get_id.available) > 0:
        return get_id.available.pop()
    else:
        get_id.id += 1
        return get_id.id
get_id.available = []
get_id.id = -1

class TiePyBase:
    '''
    the base class for all other tiepy decorators(design pattern not @). The
    decorator monitors changes in value/key(decided in child class). A value's
    value is also monitored (recursive problem here)

    Attributes:
        _callbacks (dict): the key is the id generated and the value is a tuple
            of: (owner, path, callback) where the owner is the original object
            for the callback, path is the keys/attr needed to get to the current
            value and callback is the function called
        _publish (bool): should the callback be called or not, if false the
            callback will not be invoked (used for internal changes)
        _chain([objects]): passes on a chain of accessed items to ensure there
            is not a circular reference. A set would be a better runtime
    '''
    def __init__(self, obj, owners):
        self._owners = owners
        self._callbacks = {}
        self._publish = False
        self._copy(obj)
        self._publish = True

    def __hash__(self):
        return id(self)

    def _extend_owners(self, owners={}):
        self._publish = False

        owners_diff = {}
        for owner, paths in owners.items():
            diff = paths - self._owners[owner]
            owners_diff[owner] = diff
            self._owners[owner] |= diff

        for s, v in self._get_items():
            if issubclass(v.__class__, TiePyBase): #checks for circular reference
                next_owner = {}
                for owner, paths in owners_diff.items():
                    next_owner[owner] = {p + (s,) for p in paths}
                v._extend_owners(next_owner)

        self._publish = True  

    def _run_callbacks(self, owners, value, action):
        '''
        executes all callbacks passing along the arguments above

        Args:
            step (obj): the step in the current path from owner to value
            value (obj): the new value (None if deleted)
            action (Action Enum): what action was done to get to that value
        '''
        if not self._publish:
            return

        for owner, paths in owners.items():
            for callback in owner._callbacks.values():
                callback(
                    owner=owner,
                    path=next(iter(paths)),
                    value=value,
                    action=action
                )


    def _propagate_owner(self, owner, path):
        '''
        '''
        self._owners[owner].add(path)
        for s, v in self._get_items():
            if issubclass(v.__class__, TiePyBase):
                v._propagate_owner(owner, path + (s,))
   
    def _remove_paths(self, step, value): 
        for owner, paths in self._owners.items():
            if owner not in value._owners: continue
            removed_paths = {p + (step,) for p in paths}
            value._owners[owner] -= removed_paths
            if len(value._owners[owner]) == 0:
                del value._owners[owner]
            value._remove_next_paths(owner, removed_paths, {value})
    
    def _remove_next_paths(self, owner, paths, chain):
        for s, v in self._get_items():
            if issubclass(v.__class__, TiePyBase) and v not in chain:
                removed_paths = {p + (s,) for p in paths}
                v._owners[owner] -= removed_paths
                if len(v._owners[owner]) == 0:
                    del v._owners[owner]
                v._remove_next_paths(owner, removed_paths, chain|{v})
                
                

    def subscribe(self, callback):
        '''
        on variable change, callback submitted is called, acting as a
        recursive driver for _subscribe

        Args:
            callback (function(owner, path, value, action, prior)): The function
                that gets called when a member variable changes

        Returns:
            int: the id of the subscriber
        '''
        id_ = get_id()
        self._callbacks[id_] = callback
        self._propagate_owner(self, ())
        return id_

    def unsubscribe(self, id_):
        '''
        removes the callback function with that id_ from the subscription list

        Args:
            id_: the id of the subscriber
        '''
        if id_ in self._callbacks:
            del self._callbacks[id_]

    def _copy(self, obj):
        '''
        copies the data within the object, ensuring that all points have a
        subscriber

        obj (instance of class): the object being copied
        '''
        pass

    def _get_steps(self):
        '''
        Returns:
           [obj]: the step needed to get from one above to that tie_py object,
               keys in the case of a dictionary
        '''
        pass

    def _get_values(self):
        '''
        Returns:
            [obj]: the values corresponding to each key
        '''
        pass

    def _get_items(self):
        '''
        Returns:
            iterable step value pair (s, v)
        '''
        return zip_longest(self._get_steps(), self._get_values())
