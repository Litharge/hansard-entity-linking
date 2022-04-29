import unittest
import pickle

import datetime

from mention_detection.exact_office_span_detection import get_exact_office_spans

from discourse_model.model_from_list import MPList

class TestMemberForSpanDetection(unittest.TestCase):
    def test_member_for_spans_correctly_identified_at_time(self):
        # on 2020-01-01 we would expect "The Parliamentary Under-Secretary of State" to refer to member for Torbay and
        # "the Shadow Home Secretary" to refer to member for hackney
        test_utterance = "The Parliamentary Under-Secretary of State for the Home Department met with the Parliamentary Under-Secretary (Department for Transport) and the Shadow Home Secretary"

        test_model = pickle.load(open("verified_test_discourse_model.p", "rb"))

        test_datetime = datetime.datetime(2020, 1, 1)

        result = get_exact_office_spans(test_model, test_utterance, test_datetime)

        # transform to include constituency for span only, as each MP can uniquely be identified by constituency
        results_with_constituency_only = [(item[0], item[1].constituency) for item in result]

        self.assertTrue(((0, 66), "Torbay") in results_with_constituency_only)
        self.assertTrue(((141, 166), "Hackney North and Stoke Newington") in results_with_constituency_only)
