import datetime

from mention_detection.utterance_level import Mentions

import unittest

import stanza


class TestProduceMentions(unittest.TestCase):
    def test_sentences_are_correct(self):
        test_utterance = "I am sure that I've not seen it. Myself, I would prefer to hear it from a friend of mine. Come with me. You can go in, he is friendly."

        test_sentence_spans = [(0, 32), (33, 89), (90, 103), (104, 134)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        m = Mentions(test_sentence_spans)

        dummy_datetime = datetime.datetime(2020, 1, 1)
        m.detect_mentions(doc, test_utterance, model_location="verified_test_discourse_model.p", datetime_of_utterance=dummy_datetime)

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

        dummy_datetime = datetime.datetime(2020, 1, 1)
        m.detect_mentions(doc, test_utterance, model_location="verified_test_discourse_model.p",
                          datetime_of_utterance=dummy_datetime)

        print(test_utterance)
        print(m)

        result_sentences = [a.sentence_number for a in m.annotated_mentions if a.person == None]

        self.assertListEqual(result_sentences, [0, 1, 1])

    def test_hon_genders_are_correct(self):
        test_utterance = "My right hon  friend is waiting for you. The right hon  lady and the hon  gentleman are here."

        test_sentence_spans = [(0, 40), (41, 93)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        m = Mentions(test_sentence_spans)

        dummy_datetime = datetime.datetime(2020, 1, 1)
        m.detect_mentions(doc, test_utterance, model_location="verified_test_discourse_model.p",
                          datetime_of_utterance=dummy_datetime)

        print(test_utterance)
        print(m)

        result_sentences = [a.gender for a in m.annotated_mentions if a.person == None]

        self.assertListEqual(result_sentences, ["epicene", "masculine", "feminine"])


    def test_correct_sentence_bounds(self):
        test_utterance_span = "The  hon Gentleman is at least partly correct. There will be additional costs to " \
                              "maintaining the Vanguard class through to 2028."

        nlp = stanza.Pipeline(lang='en', processors='tokenize')

        doc = nlp(test_utterance_span)

        test_obj = Mentions([])

        results = test_obj.get_sentence_bounds(doc)

        self.assertEqual(results[0], (0, 46))
        self.assertEqual(results[1], (47, 128))


    def test_speaker_sentences_are_correct(self):
        test_utterance = "Mr Speaker, the hon  gentleman is correct. Excuse me, Madam Speaker."

        test_sentence_spans = [(0, 42), (43, 68)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        m = Mentions(test_sentence_spans)

        dummy_datetime = datetime.datetime(2020, 1, 1)
        m.detect_mentions(doc, test_utterance, model_location="verified_test_discourse_model.p",
                          datetime_of_utterance=dummy_datetime)

        print(test_utterance)
        print(m)

        result_sentences = [a.sentence_number for a in m.annotated_mentions if a.role == "speaker_mention"]

        self.assertListEqual(result_sentences, [0, 1])

    def test_deputy_speaker_genders_are_correct(self):
        test_utterance = "Mr Deputy Speaker, the hon  gentleman is correct. Excuse me, Madam Deputy Speaker."

        test_sentence_spans = [(0, 49), (50, 82)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        m = Mentions(test_sentence_spans)

        dummy_datetime = datetime.datetime(2020, 1, 1)
        m.detect_mentions(doc, test_utterance, model_location="verified_test_discourse_model.p",
                          datetime_of_utterance=dummy_datetime)

        print(test_utterance)
        print(m)

        result_sentences = [a.gender for a in m.annotated_mentions if a.role == "deputy_speaker_mention"]

        self.assertListEqual(result_sentences, ["masculine", "feminine"])

if __name__ == "__main__":
    unittest.main()