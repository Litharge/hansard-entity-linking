import unittest
import json

from evaluation.statistics.measures import get_recall_for_dictionary, get_precision_for_dictionary, get_f1_for_dictionary

class TestMeasures(unittest.TestCase):
    def setUp(self):
        self.gold = json.load(open("./gold.json"))["clusters"]
        self.sys = json.load(open("sys.json"))["clusters"]
        self.small_tolerance = 0.01

    def test_get_recall_for_dictionary(self):
        recall = get_recall_for_dictionary(self.gold, self.sys)
        print("recall",recall)

        self.assertTrue(0.4-self.small_tolerance < recall < 0.4+self.small_tolerance)

    def test_get_precision_for_dictionary(self):
        precision = get_precision_for_dictionary(self.gold, self.sys)
        print("preci",precision)
        self.assertTrue(0.66 - self.small_tolerance < precision < 0.66 + self.small_tolerance)

    def test_get_f1(self):
        f1 = get_f1_for_dictionary(self.gold, self.sys)
        self.assertTrue(0.5-self.small_tolerance < f1 < 0.5+self.small_tolerance)


if __name__ == "__main__":
    unittest.main()

