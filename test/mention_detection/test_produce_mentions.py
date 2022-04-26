from mention_detection.produce_mentions import Mentions

import unittest

import stanza


class TestProduceMentions(unittest.TestCase):
    def test_sentences_are_correct(self):
        test_utterance = "I am sure that I've not seen it. Myself, I would prefer to hear it from a friend of mine. Come with me. You can go in, he is friendly."

        test_sentence_spans = [(0, 32), (33, 89), (90, 103), (104, 134)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        result = Mentions(doc, test_utterance, test_sentence_spans)

        print(test_utterance)
        print(result)

        result_sentences = [a.sentence_number for a in result.annotated_mentions]

        self.assertListEqual(result_sentences, [0, 0, 1, 1, 1, 2, 3, 3])

    def test_hon_sentences_are_correct(self):
        test_utterance = "My right hon  friend is waiting for you. The right hon  lady and the hon  gentleman are here."

        test_sentence_spans = [(0, 40), (41, 93)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        result = Mentions(doc, test_utterance, test_sentence_spans)

        print(test_utterance)
        print(result)

        result_sentences = [a.sentence_number for a in result.annotated_mentions if a.person == None]

        self.assertListEqual(result_sentences, [0, 1, 1])

    def test_hon_genders_are_correct(self):
        test_utterance = "My right hon  friend is waiting for you. They are pleased."

        test_sentence_spans = [(0,40), (41,58)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        result = Mentions(doc, test_utterance, test_sentence_spans)

        print(test_utterance)
        print(result)

        result_sentences = [a.gender for a in result.annotated_mentions if a.person == None]

        #self.assertListEqual(result_sentences, ["masculine", "feminine"])






if __name__ == "__main__":
    unittest.main()