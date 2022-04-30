import unittest
import pickle

import datetime

from mention_detection.exact_nominal_mentions import get_exact_nominal_mentions

from discourse_model.model_from_list import MPList

class TestMemberForSpanDetection(unittest.TestCase):
    def test_member_for_spans_correctly_identified_at_time(self):
        # on 2020-01-01 we would expect "The Parliamentary Under-Secretary of State" to refer to member for Torbay and
        # "the Shadow Home Secretary" to refer to member for hackney
        test_utterance = "Kevin Foster, Rachel Maclean. Diane Abbott."

        test_model = pickle.load(open("verified_test_discourse_model.p", "rb"))

        result = get_exact_nominal_mentions(test_model, test_utterance)

        for item in result:
            print(item)

        # extract ranges and the constituency associated with their associated MP, as this uniquely identifies the MP
        ranges_with_constituencies = [(item.start_char, item.end_char, item.entity.constituency) for item in result]
        print(ranges_with_constituencies)

        self.assertSetEqual(set(ranges_with_constituencies), {(0, 12, 'Torbay'), (14, 28, 'Redditch'), (30, 42, 'Hackney North and Stoke Newington')})
