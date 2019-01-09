# external modules
import unittest
from collections import defaultdict

class TestTiePyBaseList(unittest.TestCase):
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
            self.assertTrue(callback.owner is owner)
            v = owner
            try:
                for i in range(len(path)):
                    step = path[i]
                    v = v[step]
                self.assertTrue(args[0] is v)
                if method in [list.__delitem__, list.pop]:
                    pass #what can you check here? indexes are shifted
                elif method in [list.__iadd__, list.extend]:
                    obj, itr = args
                    for i in range(-1, -len(itr) - 1, -1): #go backwards
                        self.assertTrue(v[i] is itr[i])
                elif method is list.__imul__:
                    pass #is there a way you can check here?
                elif method in [list.__setitem__, list.insert]:
                    obj, index, value = args
                    self.assertTrue(index in range(len(v)))
                    self.assertTrue(value is v[index])
                elif method is list.append:
                    obj, value = args
                    self.assertTrue(len(v) > 0)
                    self.assertTrue(v[-1] is value)
                elif method is list.clear:
                    obj, = args
                    self.assertEqual(v, [])
                elif method is list.remove:
                    pass #not sure how you would check this
                elif method is list.reverse:
                    pass #not sure how you would check this

                self.callback.count[method] += 1
            except Exception as e:
                print(e)
                self.assertTrue(False)

        self.callback = callback
        self.callback.count = defaultdict(lambda: 0)
    def assert_count(self, method, expected_count):
        '''
        asserts the count is correct for a given action
        '''
        self.assertEqual(self.callback.count[method], expected_count)
