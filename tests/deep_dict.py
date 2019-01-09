# inhouse
from tie_py import tie_pyify
from tests.base_dict import TestTiePyBaseDict

class TestTiePyDeepDict(TestTiePyBaseDict):

    def test_multi_layered_general(self):
        '''
        Testing a multilevel dictionary
        '''
        x = {"A": {"B": 1, "C": {"D": 10}, }, "E": {"F": 30}}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x["A"]["B"] = 10
        self.assert_count(dict.__setitem__, 1)
        x["A"]["C"]["D"] = 25
        self.assert_count(dict.__setitem__, 2)

        m = x["A"]
        m["B"] = 35
        self.assertEqual(x["A"]["B"], 35)
        self.assert_count(dict.__setitem__, 3)

        m["B"] = {"GREG": 28}
        self.assertEqual(x["A"]["B"], m["B"])
        self.assert_count(dict.__setitem__, 4)

        m["B"]["GREG"] = 29
        self.assertEqual(x["A"]["B"]["GREG"], m["B"]["GREG"])
        self.assert_count(dict.__setitem__, 5)

        g = m
        m = {}
        m["NO"] = "YES"
        self.assert_count(dict.__setitem__, 5)

        g["NO"] = "YES"
        self.assert_count(dict.__setitem__, 6)

        g["NO"] = "YES"
        self.assert_count(dict.__setitem__, 6)

        x["A"]["NO"] = "Maybe"
        self.assert_count(dict.__setitem__, 7)

        x["E"]["F"] = "39"
        self.assert_count(dict.__setitem__, 8)

        x.unsubscribe(s_id)

        x["E"]["F"] = "12"
        self.assert_count(dict.__setitem__, 8)

    def test_multi_layered_delete_operation(self):
        x = {"A": {"B": 1, "C": {"D": 10, "G": 32}, "J": 67}, "E": {"F": 30}}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        del x["A"]["B"]
        self.assert_count(dict.__delitem__, 1)
        self.assertTrue("B" not in x["A"])

        x["A"]["C"]["D"] = 98
        self.assert_count(dict.__setitem__, 1)

        b = x["A"]
        del x["A"]
        self.assert_count(dict.__delitem__, 2)
        self.assertTrue("A" not in x)

        b["D"] = 97
        self.assert_count(dict.__setitem__, 1)

        x.unsubscribe(s_id)
