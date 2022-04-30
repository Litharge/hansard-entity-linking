import pickle
from pprint import pprint
import unittest

from mention_detection.regular_secretary import get_regular_secretary_mentions

from discourse_model.model_from_list import MPList

class TestMemberForSpanDetection(unittest.TestCase):
    def test_regular_secretary_spans_correctly_identified(self):
        test_utterance = "The Health Secretary, the Business, Energy and Industrial Strategy Secretary"

        result = get_regular_secretary_mentions(test_utterance)

        for item in result:
            print(item)

        self.assertTrue((result[0].start_char, result[0].end_char) == (0, 20))
        self.assertTrue((result[1].start_char, result[1].end_char) == (22, 76))

    def test_regular_shadow_secretary_spans_correctly_identified(self):
        test_utterance = "The shadow Health Secretary, the shadow Business, Energy and Industrial Strategy Secretary"

        result = get_regular_secretary_mentions(test_utterance)

        print("shadow result")
        for item in result:
            print(item)

        self.assertTrue((result[0].start_char, result[0].end_char) == (0, 27))
        self.assertTrue((result[1].start_char, result[1].end_char) == (29, 90))


if __name__ == "__main__":
    unittest.main()

