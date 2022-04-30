import datetime

from mention_detection.utterance_level import Mentions

import unittest

import stanza

# todo: this should only test sentence data
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

    def test_minister_class_sentences_are_correct(self):
        test_utterance = "The secretary of state, the shadow minister, the minister. The under-secretary, the shadow secretary of state."

        test_sentence_spans = [(0, 58), (59, 110)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        m = Mentions(test_sentence_spans)

        dummy_datetime = datetime.datetime(2020, 1, 1)
        m.detect_mentions(doc, test_utterance, model_location="verified_test_discourse_model.p",
                          datetime_of_utterance=dummy_datetime)

        char_in_sentence_only = [(item.start_char_in_sentence, item.end_char_in_sentence) for item in m.annotated_mentions]

        print("char in sent only")
        print(char_in_sentence_only)

        self.assertSetEqual(set(char_in_sentence_only), {(0, 22), (45, 57), (24, 43), (0, 19), (21, 50)})

    # test whether multiple mention types can be detected correctly simultaneously
    def test_multiple(self):
        test_utterance = "I see my hon  friend the shadow Health Secretary agrees. The Parliamentary Under-Secretary of State for the Home Department. Mr Speaker and Madam Deputy Speaker."

        test_sentence_spans = [(0, 56), (57, 124), (125, 161)]

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        doc = nlp(test_utterance)

        m = Mentions(test_sentence_spans)

        dummy_datetime = datetime.datetime(2020, 1, 1)
        m.detect_mentions(doc, test_utterance, model_location="verified_test_discourse_model.p",
                          datetime_of_utterance=dummy_datetime)

        for item in m.annotated_mentions:
            print(item)

        sentence_pos_with_features = [(item.sentence_number, item.start_char_in_sentence, item.end_char_in_sentence, item.shadow, item.role) for item in m.annotated_mentions]

        print(sentence_pos_with_features)

        self.assertTrue((0, 0, 1, None, None) in sentence_pos_with_features)
        self.assertTrue((0, 6, 8, None, None) in sentence_pos_with_features)
        self.assertTrue((0, 6, 20, None, None) in sentence_pos_with_features)
        self.assertTrue((0, 21, 48, True, 'secretary_regular_mention') in sentence_pos_with_features)
        self.assertTrue((1, 0, 66, None, "exact_office_match") in sentence_pos_with_features)
        self.assertTrue((2, 0, 10, None, "speaker_mention") in sentence_pos_with_features)
        self.assertTrue((2, 15, 35, None, "deputy_speaker_mention") in sentence_pos_with_features)


if __name__ == "__main__":
    unittest.main()