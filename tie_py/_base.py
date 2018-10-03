from itertools import zip_longest

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
    decorator monitors changes in value/key(decided in child class). An value's
    value is also monitored (recursive problem here)

    Attributes:
        _callbacks (dict): the key is the id generated and the value is a tuple
            of: (owner, keys, callback) where the owner is the original object
            for the callback, key is the keys/attr needed to get to the current
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

    def _extend_callbacks(self, callbacks, key=[]):
        '''
        if one ore more callback arrays are added to the system,
TODO: need to verify that the lower down keys are transmitted with the callbacks
        '''
        self._publish = False
        #ensures the correct chain of keys for each callback
        for k, v in callbacks.items():
            obj, keys, callback = v
            self._callbacks[k] = (obj, keys + key, callback)
 
        for k, v in self._get_items():
            if issubclass(v.__class__, TiePyBase):
                v._extend_callbacks(callbacks, key + [k])
        self._publish = True

    def _run_callbacks(self, value, key):
        '''
        given a value and key, invokes all the callbacks accordingly

        Args:
            value: the value changed to
            key: the key for that value
        '''
        if not self._publish:
            return
        for owner, keys, callback in self._callbacks.values():
            callback(
                owner,
                keys + [key],
                value)

    def _subscribe(self, id_, owner, prior_keys, callback):
        '''
        gets drivin by the subscribe operator

        Args:
            id_(int): the id of the callback
            owner: the originator of the subscription
            keys: the path from the owner to the value
            callback(function): gets called on variable change
        '''
        self._callbacks[id_] = (owner, prior_keys, callback)
        values = self._get_values()
        keys = self._get_keys()
        for k, v in self._get_items():
            if issubclass(v.__class__, TiePyBase):
                v._subscribe(id_, owner, prior_keys + [k], callback)

    def subscribe(self, callback):
        '''
        on variable change, callback submitted is called, acting as a
        recursive driver for __subscribe

        Args:
            callback (function(name, prior, current)): The function that gets
                called when a field variable changes

        Returns:
            int: the id of the subscriber
        '''
        id_ = get_id()
        self._subscribe(id_, self, [], callback) #self og owner
        return id_

    def _unsubscribe(self, ids=[]):
        '''
        a list of id's to unsubscribe the object from (remove callbacks), intended
        for internal use but if you're feeling confident try it out!

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
        though: revise it down to self._unsubscribe([id_]) (no for loop?)
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

    def _get_keys(self):
        '''
        Returns:
           [obj]: the keys for that tie_py object
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
            iterable key value pair (k, v)
        '''
        return zip_longest(self._get_keys(), self._get_values())
        
