# external
from collections import defaultdict

# inhouse
from tie_py import tie_pyify
from tests.base_dict import TestTiePyBaseDict

class TestTiePyComplexDict(TestTiePyBaseDict):

    def test_in_object_dict_moves(self):
        x = {"A": {"B": 1, "C": {"D": 10, "G": 32}, "J": 67}, "E": {"F": 30}}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        m = x["A"]["C"]
        x["H"] = 98
        self.assert_count(dict.__setitem__, 1)

        x["H"] = m
        self.assert_count(dict.__setitem__, 2)

        x["H"]["D"] = 99
        self.assert_count(dict.__setitem__, 3)

        x["A"]["C"] = 45
        self.assert_count(dict.__setitem__, 4)

        x["H"]["D"] = 73
        self.assert_count(dict.__setitem__, 5)

        x["N"] = 42
        self.assert_count(dict.__setitem__, 6)

	#challenge problem
        x["N"] = x
        self.assert_count(dict.__setitem__, 7)
        x["N"]["N"]["N"]["N"] = 10
        self.assert_count(dict.__setitem__, 8)

        #even more challenging
        x["A"]["B"] = x
        self.assert_count(dict.__setitem__, 9)
        x["A"]["B"]["A"]["B"] = 29
        self.assert_count(dict.__setitem__, 10)

        x.unsubscribe(s_id)

    def test_multiple_keys_to_same_object(self):
        x = {"A": {"B": 1, "C": {"D": 10, "G": 32}, "J": 67}, "E": {"F": 30}}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        m = x["A"]["C"]
        x["H"] = 98
        self.assert_count(dict.__setitem__, 1)

        x["H"] = m
        self.assert_count(dict.__setitem__, 2)

        x["H"]["D"] = 99
        self.assert_count(dict.__setitem__, 3)

        del x["H"]
        x["A"]["C"]["D"] = 120
        self.assert_count(dict.__setitem__, 4)

    def test_in_object_dict_moves_with_multiple_callbacks(self):
        x = {"A": {"B": 1, "C": {"D": 10, "G": 32}, "J": 67}, "E": {"F": 30}}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        def callback_1(owner, path, method, args):
            self.assertTrue(callback_1.owner is owner)
            v = owner
            path = list(path)
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
            elif action == dict.__delitem__:
                obj, key = args
                self.assertTrue(obj is v)
                self.assertTrue(key not in v)
            else:
                self.assertTrue(False)
            callback_1.count[method] += 1
        callback_1.count = defaultdict(lambda: 0)

        def assert_count_1(action, expected_count):
            self.assertEqual(callback_1.count[action], expected_count)


        m = {"Z": 1}
        m = tie_pyify(m)
        callback_1.owner = m
        m_id = m.subscribe(callback_1)
        m["L"] = {"T": 98}
        assert_count_1(dict.__setitem__, 1)

        x["A"]["J"] = m
        self.assert_count(dict.__setitem__, 1)
        assert_count_1(dict.__setitem__, 1)
        self.assertTrue(x["A"]["J"] == m)

        m["L"]["T"] = 99
        self.assert_count(dict.__setitem__, 2)
        assert_count_1(dict.__setitem__, 2)
