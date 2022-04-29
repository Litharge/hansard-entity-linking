import pickle
from pprint import pprint
import unittest

from mention_detection.ministerial_class_span_detection import get_ministerial_class_mentions

from discourse_model.model_from_list import MPList

class TestMemberForSpanDetection(unittest.TestCase):
    def test_member_for_spans_correctly_identified(self):
        test_utterance = "The secretary of state, the shadow minister, the minister, the under-secretary, the shadow secretary of state"

        result = get_ministerial_class_mentions(test_utterance)


        chars_only = [(item.start_char, item.end_char) for item in result]

        print(chars_only)

        self.assertSetEqual(set(chars_only), {(0, 22), (24, 43), (45, 57), (59, 78), (80, 109)})


if __name__ == "__main__":
    unittest.main()

