import json
import unittest

from evaluation.statistics.binary_classification import get_false_negative, get_true_positive, get_false_positive

class TestBinaryClassification(unittest.TestCase):
    def setUp(self):
        self.gold = json.load(open("./gold.json"))["clusters"]
        self.sys = json.load(open("sys.json"))["clusters"]

    def test_true_positive(self):
        true_positive = get_true_positive(self.gold, self.sys)
        print(true_positive)
        self.assertTrue(true_positive == 2)

    def test_false_negative(self):
        false_negative = get_false_negative(self.gold, self.sys)
        print(false_negative)
        self.assertTrue(false_negative == 3)

    def test_false_positive(self):
        false_positive = get_false_positive(self.gold, self.sys)
        print("false pos", false_positive)
        self.assertTrue(false_positive == 1)


if __name__ == "__main__":
    unittest.main()