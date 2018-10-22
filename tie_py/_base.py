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
    def __init__(self, obj, callbacks={}):
        self._chain = []
        self._callbacks = callbacks
        self._publish = False
        self._copy(obj)
        self._publish = True

    def _extend_callbacks(self, callbacks, ext_path=[]):
        '''
        if one ore more callback arrays are added to the system

        Args:
            callbacks ([(owner, path, callback)]): list of callbacks being added
            ext_path (list): the additional path that needs to be appended to
                the current callbacks path
        '''
        self._publish = False
        #ensures the correct chain of keys for each callback
        for id_, v in callbacks.items():
            owner, path, callback = v
            self._callbacks[id_] = (owner, path + ext_path, callback)

        for s, v in self._get_items():
            if issubclass(v.__class__, TiePyBase):
                v._extend_callbacks(callbacks, ext_path + [s])
        self._publish = True

    def _run_callbacks(self, step, value, action):#we should have the function called too
        '''
        executes all callbacks passing along the arguments above

        Args:
            step (obj): the step in the current path from owner to value
            value (obj): the new value (None if deleted)
            action (Action Enum): what action was done to get to that value
        '''
        if not self._publish:
            return

        for owner, path, callback in self._callbacks.values():
            callback(
                owner=owner,
                path=path + [step],
                value=value,
                action=action
                )

    def _subscribe(self, id_, owner, prior_path, callback):
        '''
        gets drivin by the subscribe operator

        Args:
            id_(int): the id of the callback
            owner (obj): the originator of the subscription
            prior_path([obj]): the path from the owner to the value
            callback(function): gets called on variable change
        '''
        self._callbacks[id_] = (owner, prior_path, callback)
        for s, v in self._get_items():
            if issubclass(v.__class__, TiePyBase):
                v._subscribe(id_, owner, prior_path + [s], callback)

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
        self._subscribe(id_, self, [], callback) #self is the og owner
        return id_

    def _unsubscribe(self, ids=[]):
        '''
        a list of id's to unsubscribe the object from (remove callbacks),
        intended for internal use but if you're feeling confident try it out!

        Args:
            ids ([int]): the list of ids that are being unsubscribed from
        '''
        for id_ in ids:
            if id_ in self._callbacks:
               owner, _, _ = self._callbacks[id_]
               if owner is self and id_ not in get_id.available:
                   get_id.available.append(id_)
               del self._callbacks[id_]

            for v in self._get_values():
                if issubclass(v.__class__, TiePyBase):
                    v._unsubscribe(ids)
    def unsubscribe(self, id_):
        '''
        removes the callback function with that id_ from the subscription list

        Args:
            id_: the id of the subscriber
        '''
        if id_ in self._callbacks:
            self._unsubscribe([id_])

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
