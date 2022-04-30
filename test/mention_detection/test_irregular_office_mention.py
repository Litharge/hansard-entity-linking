import unittest
import pickle

import datetime

from mention_detection.irregular_office_mention import get_irregular_office_mentions

from discourse_model.model_from_list import MPList


class TestMemberForSpanDetection(unittest.TestCase):
    def test_irregular_office_mentions(self):
        # on 2020-01-01 we would expect "The Parliamentary Under-Secretary of State" to refer to member for Torbay and
        # "the Shadow Home Secretary" to refer to member for hackney
        test_utterance = "The Paymaster General, the Prime Minister, the Deputy Prime Minister, the Chancellor, the Lord Chancellor, the Leader of the Opposition"

        result = get_irregular_office_mentions(test_utterance)

        spans_only = [(item.start_char, item.end_char) for item in result]

        self.assertSetEqual(set(spans_only), {(0, 21), (23, 41), (43, 68), (70, 84), (86, 105), (107, 135)})
