# external modules
import unittest
from collections import defaultdict

class TestTiePyBaseDict(unittest.TestCase):
    '''
    runs tests on:

    '''
    callback = None

    def setUp(self):
        '''
        Called before every test function, must set static obj
        in the test function itself
        '''
        def callback(owner, path, method, args):
            path = list(path)
            self.assertTrue(callback.owner is owner)

            #follows the path down
            v = owner
            while len(path) > 0:
                k = path.pop(0)
                if k in v:
                    v = v[k]
                else:
                    self.assertTrue(False)
            if method == dict.__setitem__:
                obj, key, value = args
                self.assertTrue(obj is v)
                self.assertTrue(key in v)
                self.assertTrue(value is v[key])
            elif method == dict.__delitem__:
                obj, key = args
                self.assertTrue(obj is v)
                self.assertTrue(key not in v)
                self.assertTrue(len(path) == 0)
            else:
                self.assertTrue(False)

            self.callback.count[method] += 1

        self.callback = callback
        self.callback.count = defaultdict(lambda: 0)

    def assert_count(self, method, expected_count):
        '''
        asserts the count is correct for a given action
        '''
        self.assertEqual(self.callback.count[method], expected_count)
