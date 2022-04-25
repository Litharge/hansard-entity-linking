from mention_detection.produce_mentions import get_sentence_bounds, transform_hon
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

    def test_correct_sentence_bounds(self):
        test_utterance_span = "The  hon Gentleman is at least partly correct. There will be additional costs to " \
                              "maintaining the Vanguard class through to 2028."

        nlp = stanza.Pipeline(lang='en', processors='tokenize')

        results = get_sentence_bounds(nlp, test_utterance_span)

        self.assertEqual(results[0], (0, 46))
        self.assertEqual(results[1], (47, 128))


if __name__ == "__main__":
    unittest.main()

