import datetime
import pickle

from structure.utterance_level import Mentions

import unittest

import stanza

# todo: this should only test sentence data
class TestProduceMentions(unittest.TestCase):
    def test_sentences_are_correct(self):
        test_utterance = "I am sure that I've not seen it. Myself, I would prefer to hear it from a friend of mine. Come with me. You can go in, he is friendly."

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        m = Mentions()

        dummy_datetime = datetime.datetime(2020, 1, 1)
        model_location = "verified_test_discourse_model.p"
        model = pickle.load(open(model_location, "rb"))

        m.detect_mentions(nlp, test_utterance, model=model, datetime_of_utterance=dummy_datetime)

        print(test_utterance)
        print(m)

        result_sentences = [a.sentence_number for a in m.annotated_mentions]

        self.assertListEqual(result_sentences, [0, 0, 1, 1, 1, 2, 3, 3])

    def test_hon_sentences_are_correct(self):
        test_utterance = "My right hon  friend is waiting for you. The right hon  lady and the hon  gentleman are here."

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        m = Mentions()

        dummy_datetime = datetime.datetime(2020, 1, 1)
        model_location = "verified_test_discourse_model.p"
        model = pickle.load(open(model_location, "rb"))

        m.detect_mentions(nlp, test_utterance, model=model,
                          datetime_of_utterance=dummy_datetime)

        print(test_utterance)
        print(m)

        result_sentences = [a.sentence_number for a in m.annotated_mentions if a.person == None]

        self.assertListEqual(result_sentences, [0, 1, 1])

    def test_hon_genders_are_correct(self):
        test_utterance = "My right hon  friend is waiting for you. The right hon  lady and the hon  gentleman are here."

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        m = Mentions()

        dummy_datetime = datetime.datetime(2020, 1, 1)
        model_location = "verified_test_discourse_model.p"
        model = pickle.load(open(model_location, "rb"))

        m.detect_mentions(nlp, test_utterance, model=model,
                          datetime_of_utterance=dummy_datetime)

        print(test_utterance)
        print(m)

        result_sentences = [a.gender for a in m.annotated_mentions if a.person == None]

        self.assertListEqual(result_sentences, ["epicene", "masculine", "feminine"])


    def test_correct_sentence_bounds(self):
        test_utterance = "The  hon Gentleman is at least partly correct. There will be additional costs to " \
                              "maintaining the Vanguard class through to 2028."

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        m = Mentions()

        dummy_datetime = datetime.datetime(2020, 1, 1)
        model_location = "verified_test_discourse_model.p"
        model = pickle.load(open(model_location, "rb"))

        m.detect_mentions(nlp, test_utterance, model=model,
                          datetime_of_utterance=dummy_datetime)

        self.assertEqual(m.sentence_bounds[0], (0, 46))
        self.assertEqual(m.sentence_bounds[1], (47, 128))


    def test_speaker_sentences_are_correct(self):
        test_utterance = "Mr Speaker, the hon  gentleman is correct. Excuse me, Madam Speaker."

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        m = Mentions()

        dummy_datetime = datetime.datetime(2020, 1, 1)
        model_location = "verified_test_discourse_model.p"
        model = pickle.load(open(model_location, "rb"))

        m.detect_mentions(nlp, test_utterance, model=model,
                          datetime_of_utterance=dummy_datetime)

        print(test_utterance)
        print(m)

        result_sentences = [a.sentence_number for a in m.annotated_mentions if a.role == "speaker_mention"]

        self.assertListEqual(result_sentences, [0, 1])

    def test_deputy_speaker_genders_are_correct(self):
        test_utterance = "Mr Deputy Speaker, the hon  gentleman is correct. Excuse me, Madam Deputy Speaker."

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        m = Mentions()

        dummy_datetime = datetime.datetime(2020, 1, 1)
        model_location = "verified_test_discourse_model.p"
        model = pickle.load(open(model_location, "rb"))

        m.detect_mentions(nlp, test_utterance, model=model,
                          datetime_of_utterance=dummy_datetime)

        print(test_utterance)
        print(m)

        result_sentences = [a.gender for a in m.annotated_mentions if a.role == "deputy_speaker_mention"]

        self.assertListEqual(result_sentences, ["masculine", "feminine"])

    def test_minister_class_sentences_are_correct(self):
        test_utterance = "The secretary of state, the shadow minister, the minister. The under-secretary, the shadow secretary of state."

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        m = Mentions()

        dummy_datetime = datetime.datetime(2020, 1, 1)
        model_location = "verified_test_discourse_model.p"
        model = pickle.load(open(model_location, "rb"))

        m.detect_mentions(nlp, test_utterance, model=model,
                          datetime_of_utterance=dummy_datetime)

        char_in_sentence_only = [(item.start_char_in_sentence, item.end_char_in_sentence) for item in m.annotated_mentions]

        print("char in sent only")
        print(char_in_sentence_only)

        self.assertSetEqual(set(char_in_sentence_only), {(0, 22), (45, 57), (24, 43), (0, 19), (21, 50)})

    # test whether multiple mention types can be detected correctly simultaneously
    def test_multiple(self):
        test_utterance = "I see my hon  friend the shadow Health Secretary agrees, he is right. The Parliamentary Under-Secretary of State for the Home Department. Mr Speaker and Madam Deputy Speaker, the member for Redditch. Diane Abbott. The Prime Minister."

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        m = Mentions()

        dummy_datetime = datetime.datetime(2020, 1, 1)
        model_location = "verified_test_discourse_model.p"
        model = pickle.load(open(model_location, "rb"))

        m.detect_mentions(nlp, test_utterance, model=model,
                          datetime_of_utterance=dummy_datetime)

        for item in m.annotated_mentions:
            print(item)

        sentence_pos_with_features = [(item.sentence_number, item.start_char_in_sentence, item.end_char_in_sentence, item.person, item.gender, item.role, item.get_associated_constituency()) for item in m.annotated_mentions]

        print(sentence_pos_with_features)

        self.assertTrue((0, 0, 1, 1, None, 'pronominal_mention', None) in sentence_pos_with_features)
        self.assertTrue((0, 6, 8, 1, None, 'pronominal_mention', None) in sentence_pos_with_features)
        self.assertTrue((0, 57, 59, 3, 'masculine', 'pronominal_mention', None) in sentence_pos_with_features)
        self.assertTrue((0, 6, 20, None, 'epicene', 'hon_mention', None) in sentence_pos_with_features)
        self.assertTrue((2, 0, 10, None, None, 'speaker_mention', None) in sentence_pos_with_features)
        self.assertTrue((2, 15, 35, None, 'feminine', 'deputy_speaker_mention', None) in sentence_pos_with_features)
        self.assertTrue((2, 37, 60, None, None, 'member_for_mention', 'Redditch') in sentence_pos_with_features)
        self.assertTrue((1, 0, 66, None, None, 'exact_office_mention', None) in sentence_pos_with_features)
        self.assertTrue((3, 0, 12, None, None, 'exact_nominal_mention', 'Hackney North and Stoke Newington') in sentence_pos_with_features)
        self.assertTrue((0, 21, 48, None, None, 'secretary_regular_mention', None) in sentence_pos_with_features)
        self.assertTrue((4, 0, 18, None, None, 'irregular_office_mention', None) in sentence_pos_with_features)

    # test whether multiple mention types can be detected correctly simultaneously
    def test_overlap_removal(self):
        # "The Shadow Home Secretary" will be detected both by the exact office match and by the regular secretary match
        test_utterance = "The Shadow Home Secretary. She"

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        m = Mentions()

        # at this date Diane Abbott was shadow home secretary
        dummy_datetime = datetime.datetime(2018, 1, 1)
        model_location = "verified_test_discourse_model.p"
        model = pickle.load(open(model_location, "rb"))

        m.detect_mentions(nlp, test_utterance, model=model,
                          datetime_of_utterance=dummy_datetime)

        for item in m.annotated_mentions:
            print(item)

        sentence_pos_with_features = [(item.sentence_number, item.start_char_in_sentence, item.end_char_in_sentence,
                                       item.is_shadow, item.role, item.get_associated_constituency()) for item in
                                      m.annotated_mentions]

        print(sentence_pos_with_features)

    def test_apposition_processing(self):
        # "The Shadow Home Secretary" will be detected both by the exact office match and by the regular secretary match
        test_utterance = "the Shadow Secretary, the hon  Member for Hackney North and Stoke Newington (Diane Abbott) " \
                         "is here. My hon  Friend the Member for Redditch (Rachel Maclean) is also here. I see my " \
                         "hon  friend the shadow Health Secretary agrees, he is right."

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
        m = Mentions()

        # at this date Diane Abbott was shadow home secretary
        dummy_datetime = datetime.datetime(2018, 1, 1)
        model_location = "verified_test_discourse_model.p"
        model = pickle.load(open(model_location, "rb"))

        m.detect_mentions(nlp, test_utterance, model=model,
                          datetime_of_utterance=dummy_datetime)
        print("unsorted")
        for item in m.annotated_mentions:
            print(item)

        m.join_appositives(test_utterance)

        print("sorted")
        for item in m.annotated_mentions:
            print(item)

        sentence_pos_with_features = [(item.sentence_number, item.start_char_in_sentence, item.end_char_in_sentence,
                                       item.is_shadow, item.role, item.get_associated_constituency(), item.is_appositive) for item in
                                      m.annotated_mentions]

        print("sentence pos w feats:", sentence_pos_with_features)

        self.assertTrue((0, 0, 90, None, 'member_for_mention', 'Hackney North and Stoke Newington', True) in sentence_pos_with_features)
        self.assertTrue((1, 0, 2, None, 'pronominal_mention', None, False) in sentence_pos_with_features)
        self.assertTrue((1, 0, 55, None, 'member_for_mention', 'Redditch', True) in sentence_pos_with_features)
        self.assertTrue((2, 0, 1, None, 'pronominal_mention', None, False) in sentence_pos_with_features)
        self.assertTrue((2, 6, 8, None, 'pronominal_mention', None, False) in sentence_pos_with_features)
        self.assertTrue((2, 6, 48, True, 'secretary_regular_mention', None, True) in sentence_pos_with_features)
        self.assertTrue((2, 57, 59, None, 'pronominal_mention', None, False) in sentence_pos_with_features)

if __name__ == "__main__":
    unittest.main()