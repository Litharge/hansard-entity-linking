from mention_detection.produce_mentions import Mentions, transform_hon
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

        doc = nlp(test_utterance_span)

        test_obj = Mentions([])

        results = test_obj.get_sentence_bounds(doc)

        self.assertEqual(results[0], (0, 46))
        self.assertEqual(results[1], (47, 128))


if __name__ == "__main__":
    unittest.main()

