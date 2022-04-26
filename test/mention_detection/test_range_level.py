from mention_detection.range_level import transform_hon
import unittest
import stanza


class TestMentions(unittest.TestCase):
    def test_hon_transform(self):
        test_utterance_span_original = "The hon. Gentleman is at least partly correct. There will be additional costs to " \
                              "maintaining the Vanguard class through to 2028."

        test_utterance_span = transform_hon(test_utterance_span_original)

        test_utterance_span_expected = "The hon  Gentleman is at least partly correct. There will be additional costs to " \
                                       "maintaining the Vanguard class through to 2028."

        self.assertEqual(test_utterance_span, test_utterance_span_expected)




if __name__ == "__main__":
    unittest.main()

