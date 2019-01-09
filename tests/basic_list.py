# inhouse
from tests.base_list import TestTiePyBaseList
from tie_py import tie_pyify

class TestTiePyList(TestTiePyBaseList):

    def test_one_layered_set(self):
        '''
        Testing one subscriber on a list that's already
        been made before hand
        '''
        x = [1, 2, 3]
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x[0] = 1
        self.assert_count(list.__setitem__, 0)
        self.assertEqual(x, [1, 2, 3])

        x[0] = 0
        self.assert_count(list.__setitem__, 1)
        self.assertEqual(x, [0, 2, 3])

        x[2] = -100
        self.assert_count(list.__setitem__, 2)
        self.assertEqual(x, [0, 2, -100])

        x[0] += 1
        self.assert_count(list.__setitem__, 3)
        self.assertEqual(x, [1, 2, -100])

        x[-1] = 12
        self.assert_count(list.__setitem__, 4)
        self.assertEqual(x, [1, 2, 12])

        #unsubscribing
        x.unsubscribe(s_id)
        x[2] = 25
        self.assert_count(list.__setitem__, 4)
        self.assertEqual(x[2], 25)

    def test_one_layered_append(self):
        '''
        Testing one subscriber on a dictionary that's empty
        and new items will be added to it
        '''
        x = tie_pyify([])
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x.append(0)
        self.assert_count(list.append, 1)
        self.assertEqual(x, [0])
        x[0] = 12
        self.assert_count(list.__setitem__, 1)

        x.append(2)
        self.assert_count(list.append, 2)
        self.assertEqual(x, [12, 2])
        x[1] = 32
        self.assert_count(list.__setitem__, 2)

        x.append(3)
        self.assertEqual(x, [12, 32, 3])
        self.assert_count(list.append, 3)

        #unsubscribing
        x.unsubscribe(s_id)
        x[0] = 25
        self.assert_count(list.__setitem__, 2)
        x.append(3)
        self.assert_count(list.append, 3)

    def test_one_layered_delitem(self):
        x = tie_pyify([1, 2, 3])
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        del x[2]
        self.assert_count(list.__delitem__, 1)
        self.assertEqual(x, [1, 2])

        del x[0]
        self.assert_count(list.__delitem__, 2)
        self.assertEqual(x, [2])

        del x[-1]
        self.assert_count(list.__delitem__, 3)
        self.assertEqual(x, [])

        x.append(2)
        x.append(1)
        x.append(2)
        self.assert_count(list.append, 3)

        del x[-2]
        self.assert_count(list.__delitem__, 4)
        self.assertEqual(x, [2, 2])

        x.unsubscribe(s_id)
        del x[0]
        self.assert_count(list.__delitem__, 4)

    def test_one_layered_pop(self):
        x = tie_pyify([1, 2, 3])
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        self.assertEqual(x.pop(2), 3)
        self.assert_count(list.pop, 1)
        self.assert_count(list.__delitem__, 0)
        self.assertEqual(x, [1, 2])

        self.assertEqual(x.pop(0), 1)
        self.assert_count(list.pop, 2)
        self.assertEqual(x, [2])

        self.assertEqual(x.pop(), 2)
        self.assert_count(list.pop, 3)
        self.assertEqual(x, [])

        x.append(2)
        x.append(1)
        x.append(2)
        self.assert_count(list.append, 3)

        self.assertEqual(x.pop(-2), 1)
        self.assert_count(list.pop, 4)
        self.assertEqual(x, [2, 2])

        x.unsubscribe(s_id)
        x.pop(0)
        self.assert_count(list.pop, 4)

    def test_one_layered_extend(self):
        x = tie_pyify([1, 2])
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x.extend([4, 5])
        self.assert_count(list.__setitem__, 0)
        self.assert_count(list.extend, 1)

        x.extend([])
        self.assert_count(list.extend, 2)

        x.extend([1])
        self.assert_count(list.extend, 3)

        self.assertEqual(x, [1, 2, 4, 5, 1])

        #unsubscribing
        x.unsubscribe(s_id)
        x.extend([2, 3])
        self.assert_count(list.extend, 3)
        self.assertEqual(x[-2:], [2, 3])

    def test_one_layered_iadd(self):
        x = tie_pyify([1, 2])
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x += [4, 5]
        self.assert_count(list.__setitem__, 0)
        self.assert_count(list.__iadd__, 1)

        x += []
        self.assert_count(list.__iadd__, 2)

        x += [1]
        self.assert_count(list.__iadd__, 3)

        self.assertEqual(x, [1, 2, 4, 5, 1])

        #unsubscribing
        x.unsubscribe(s_id)
        x += [2, 3]
        self.assert_count(list.__iadd__, 3)

    def test_one_layered_clear(self):
        x = tie_pyify([1, 2, 3, 4])
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x.clear()
        self.assert_count(list.clear, 1)
        self.assertEqual(x, [])

        x.append(1)
        self.assert_count(list.append, 1)
        self.assert_count(list.clear, 1)
        self.assertEqual(x, [1])

        x.clear()
        self.assert_count(list.clear, 2)
        self.assertEqual(x, [])

        x.clear()
        self.assert_count(list.clear, 3)
        self.assertEqual(x, [])

        #unsubscribing
        x.unsubscribe(s_id)
        x.clear()
        self.assert_count(list.clear, 3)

    def test_one_layered_insert(self):
        x = tie_pyify([1, 2, 3, 4])
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x.insert(1, 10)
        self.assert_count(list.insert, 1)
        self.assertEqual(x, [1, 10, 2, 3, 4])

        x.insert(-1, 58)
        self.assert_count(list.insert, 2)
        self.assertEqual(x, [1, 10, 2, 3, 58, 4])

        x.insert(len(x), 900)
        self.assert_count(list.insert, 3)
        self.assertEqual(x, [1, 10, 2, 3, 58, 4, 900])

        x.insert(10000, -4)
        self.assert_count(list.insert, 4)
        self.assertEqual(x, [1, 10, 2, 3, 58, 4, 900, -4])

        x.insert(-100, 2)
        self.assert_count(list.insert, 5)
        self.assertEqual(x, [2, 1, 10, 2, 3, 58, 4, 900, -4])

        x.insert(0, 12)
        self.assert_count(list.insert, 6)
        self.assertEqual(x, [12, 2, 1, 10, 2, 3, 58, 4, 900, -4])

        #unsubscribing
        x.unsubscribe(s_id)
        x.insert(2, 10)
        self.assert_count(list.insert, 6)

    def test_one_layered_remove(self):
        x = tie_pyify([1, 2, 3, 4, 1, 4])
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x.remove(1)
        self.assert_count(list.remove, 1)
        self.assertEqual(x, [2, 3, 4, 1, 4])

        x.remove(4)
        self.assert_count(list.remove, 2)
        self.assertEqual(x, [2, 3, 1, 4])

        x.remove(4)
        self.assert_count(list.remove, 3)
        self.assertEqual(x, [2, 3, 1])

    def test_one_layered_reversed(self):
        x = tie_pyify([1, 2, 3, 4])
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x.reverse()
        self.assert_count(list.reverse, 1)
        self.assertEqual(x, [4, 3, 2, 1])

        x.pop()
        x.reverse()
        self.assert_count(list.reverse, 2)
        self.assert_count(list.pop, 1)
        self.assertEqual(x, [2, 3, 4])

        x.clear()
        x.reverse()
        self.assert_count(list.reverse, 3)
        self.assert_count(list.clear, 1)
        self.assertEqual(x, [])

    def test_one_layered_imul(self):
        x = tie_pyify([1, 2, 3])
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x *= 3
        self.assert_count(list.__imul__, 1)
        self.assertEqual(x, [1, 2, 3, 1, 2, 3, 1, 2, 3])

        x *= -5
        self.assert_count(list.__imul__, 2)
        self.assertEqual(x, [])
