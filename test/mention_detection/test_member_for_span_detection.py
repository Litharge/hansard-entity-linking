import unittest
import pickle

from mention_detection.member_for_span_detection import get_member_for_spans

from discourse_model.model_from_list import MPList

class TestMemberForSpanDetection(unittest.TestCase):
    def test_member_for_spans_correctly_identified(self):
        test_utterance = "I have talked to the member for Hackney North and Stoke Newington, as well as the hon  member for Redditch. The member for Torbay, but not the Member for the Forest of Dean."

        test_model = pickle.load(open("verified_test_discourse_model.p", "rb"))

        result = get_member_for_spans(test_model, test_utterance)

        # transform to include constituency for span only, as each MP can uniquely be identified by constituency
        results_with_constituency_only = [(item[0], item[1].constituency) for item in result]

        self.assertTrue(((17, 65), "Hackney North and Stoke Newington") in results_with_constituency_only)
        self.assertTrue(((78, 106), "Redditch") in results_with_constituency_only)
        self.assertTrue(((108, 129), "Torbay") in results_with_constituency_only)


