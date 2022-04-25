from mention_detection.produce_mentions import Mentions

import unittest


class TestProduceMentions(unittest.TestCase):
    def test_sentences_are_correct(self):
        test_utterance = "I am sure that I've not seen it. Myself, I would prefer to hear it from a friend of mine. Come with me."
        test_mention_spans = [(0, 1), (15, 16), (33, 39), (41, 42), (84, 88), (100, 102)]
        test_sentence_spans = [(0, 32), (33, 89), (90, 103)]

        result = Mentions(test_mention_spans, test_sentence_spans)

        print("---")
        print(result)
        result_sentences = [a.sentence_number for a in result.annotated_mentions]

        print(result_sentences)

        self.assertListEqual(result_sentences, [0, 0, 1, 1, 1, 2])




if __name__ == "__main__":
    unittest.main()