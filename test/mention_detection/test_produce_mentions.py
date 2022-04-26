from mention_detection.produce_mentions import Mentions

import unittest

import stanza


class TestProduceMentions(unittest.TestCase):
    def test_sentences_are_correct(self):
        test_utterance = "I am sure that I've not seen it. Myself, I would prefer to hear it from a friend of mine. Come with me. You can go in, he is friendly."

        test_sentence_spans = [(0, 32), (33, 89), (90, 103), (104, 134)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        m = Mentions(test_sentence_spans)

        m.detect_mentions(doc, test_utterance)

        print(test_utterance)
        print(m)

        result_sentences = [a.sentence_number for a in m.annotated_mentions]

        self.assertListEqual(result_sentences, [0, 0, 1, 1, 1, 2, 3, 3])

    def test_hon_sentences_are_correct(self):
        test_utterance = "My right hon  friend is waiting for you. The right hon  lady and the hon  gentleman are here."

        test_sentence_spans = [(0, 40), (41, 93)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        m = Mentions(test_sentence_spans)

        m.detect_mentions(doc, test_utterance)

        print(test_utterance)
        print(m)

        result_sentences = [a.sentence_number for a in m.annotated_mentions if a.person == None]

        self.assertListEqual(result_sentences, [0, 1, 1])

    def test_hon_genders_are_correct(self):
        test_utterance = "My right hon  friend is waiting for you. They are pleased."

        test_sentence_spans = [(0,40), (41,58)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        m = Mentions(test_sentence_spans)

        m.detect_mentions(doc, test_utterance)

        print(test_utterance)
        print(m)

        result_sentences = [a.gender for a in m.annotated_mentions if a.person == None]

        #self.assertListEqual(result_sentences, ["masculine", "feminine"])


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