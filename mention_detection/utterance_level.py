# module to produce pronoun mentions

import re
import bisect
import pickle

import stanza
from lxml import etree

from mention_detection.span_detection import get_hon_epicene_mentions, \
    get_hon_masculine_mentions, \
    get_hon_feminine_mentions, \
    get_speaker_mentions, \
    get_deputy_speaker_masculine_mentions, \
    get_deputy_speaker_feminine_mentions

from mention_detection.member_for_span_detection import get_member_for_spans

from mention_detection.exact_office_span_detection import get_exact_office_spans

from mention_detection.annotated_mention import AnnotatedMention

from mention_detection.ministerial_class_span_detection import get_ministerial_class_mentions

from mention_detection.regular_secretary import get_regular_secretary_mentions

from mention_detection.exact_nominal_mentions import get_exact_nominal_mentions

from mention_detection.irregular_office_mention import get_irregular_office_mentions


# contains AnnotatedMention's
# has an id associated
class Mentions():
    def __init__(self, sentence_bounds):
        self.annotated_mentions = []

        # todo: this should be instance variable instead of arg
        self.sentence_starts = [item[0] for item in sentence_bounds]

        # store sentence bounds for conversions
        self.sentence_bounds = sentence_bounds


    # method that for a given utterance span utt_span and its corresponding stanza Document doc, adds mentions of
    # all relevant kinds to self.annotated_mentions
    def detect_mentions(self, doc, utt_span, model_location, datetime_of_utterance):
        model = pickle.load(open(model_location, "rb"))

        sentence_starts = self.sentence_starts

        self.add_pronouns(doc, sentence_starts)

        epicene_ranges = get_hon_epicene_mentions(utt_span, sentence_starts)
        self.add_am("epicene", epicene_ranges, sentence_starts)

        masculine_ranges = get_hon_masculine_mentions(utt_span, sentence_starts)
        self.add_am("masculine", masculine_ranges, sentence_starts)

        feminine_ranges = get_hon_feminine_mentions(utt_span, sentence_starts)
        self.add_am("feminine", feminine_ranges, sentence_starts)

        speaker_ranges = get_speaker_mentions(utt_span)
        self.add_am(None, speaker_ranges, sentence_starts, role="speaker_mention")

        masculine_deputy_speaker_ranges = get_deputy_speaker_masculine_mentions(utt_span)
        self.add_am("masculine", masculine_deputy_speaker_ranges, sentence_starts, role="deputy_speaker_mention")

        feminine_deputy_speaker_ranges = get_deputy_speaker_feminine_mentions(utt_span)
        self.add_am("feminine", feminine_deputy_speaker_ranges, sentence_starts, role="deputy_speaker_mention")

        member_for_ranges_and_entities = get_member_for_spans(model, utt_span)
        self.known_add_am(None, member_for_ranges_and_entities, sentence_starts, role="member_for_mention")

        exact_offices_ranges_and_entities = get_exact_office_spans(model, utt_span, datetime_of_utterance)
        self.add_am(None, exact_offices_ranges_and_entities, sentence_starts, role="exact_office_match")

        ministerial_class_mentions = get_ministerial_class_mentions(utt_span)
        self.add_am_list(ministerial_class_mentions, sentence_starts)

        regular_secretary_mentions = get_regular_secretary_mentions(utt_span)
        self.add_am_list(regular_secretary_mentions, sentence_starts)

        exact_nominal_mentions = get_exact_nominal_mentions(model, utt_span)
        self.add_am_list(exact_nominal_mentions, sentence_starts)

        irregular_office_mentions = get_irregular_office_mentions(utt_span)
        self.add_am_list(irregular_office_mentions, sentence_starts)


    # returns a tuple [start char index, end char index) for a sentence
    def get_sentence_bounds(self, doc):
        # dictionary containing sentence number as key and tuple of start and end char inclusive
        sentence_list = []

        for sentence in doc.sentences:
            sentence_list.append((sentence.tokens[0].start_char, sentence.tokens[-1].end_char))

        return sentence_list

    # returns a tuple (sentence number, index of start character within sentence, index of end character within
    # sentence)
    def get_sentence_position(self, sentence_starts, start_char, end_char):
        sentence_number = bisect.bisect_right(sentence_starts, start_char) - 1

        start_char_in_sentence = start_char - sentence_starts[sentence_number]
        end_char_in_sentence = end_char - sentence_starts[sentence_number]

        return sentence_number, start_char_in_sentence, end_char_in_sentence

    def add_am_list(self, mentions, sentence_starts):
        for mention in mentions:
            mention.sentence_number, mention.start_char_in_sentence, mention.end_char_in_sentence = self.get_sentence_position(sentence_starts,
                                                                                                       mention.start_char,
                                                                                                       mention.end_char)
            self.annotated_mentions.append(mention)

    # using a list of found span tuples, add AnnotatedMentions to self.annotated_mentions
    def add_am(self, gender, found_spans, sentence_starts, role=None):
        for mention in found_spans:
            sentence_number, start_char_in_sentence, end_char_in_sentence = self.get_sentence_position(sentence_starts, mention[0], mention[1])

            new_am = AnnotatedMention(start_char=mention[0],
                                      end_char=mention[1],
                                      sentence=sentence_number,
                                      start_char_in_sentence=start_char_in_sentence,
                                      end_char_in_sentence=end_char_in_sentence,
                                      person=None,
                                      gender=gender,
                                      role=role)

            self.annotated_mentions.append(new_am)


    def known_add_am(self, gender, found_ranges_with_entities, sentence_starts, role=None):
        for mention, entity in found_ranges_with_entities:
            sentence_number, start_char_in_sentence, end_char_in_sentence = self.get_sentence_position(sentence_starts, mention[0], mention[1])

            new_am = AnnotatedMention(start_char=mention[0],
                                      end_char=mention[1],
                                      sentence=sentence_number,
                                      start_char_in_sentence=start_char_in_sentence,
                                      end_char_in_sentence=end_char_in_sentence,
                                      person=None,
                                      gender=gender,
                                      role=role,
                                      entity=entity)

            self.annotated_mentions.append(new_am)



    def add_pronouns(self, doc, sentence_starts):
        len_of_person = len("Person=")
        len_of_gender = len("Gender=")

        # add pronouns to annotated_mentions
        for sent_no, sentence in enumerate(doc.sentences):
            for word in sentence.words:

                if word.feats is not None:
                    # if the word is a pronoun, look at the feats string to determine if the pronoun is singular
                    if word.upos == "PRON":
                        # filter out neuter and epicene pronouns, feats does not contain information to discriminate
                        if word.text.lower() in ["it", "itself", "its", "they", "them", "themselves", "theirs", "their"]:
                            continue

                        # filter out first person plural, geats does not contain info to discriminate this
                        if word.text.lower() in ["we", "us", "ourselves", "ours", "our"]:
                            continue
                        print(word.text, word.parent.text, word.upos, word.feats)

                        person = word.feats[word.feats.find("Person=")+len_of_person]

                        gender=None

                        print("word:", word.text, "gender:", word.feats[word.feats.find("Gender=")+len_of_gender : word.feats.find("Gender=")+len_of_gender+4])

                        if word.feats.find("Gender=") != -1:
                            if word.feats[word.feats.find("Gender=")+len_of_gender : word.feats.find("Gender=")+len_of_gender+4] == "Masc":
                                gender = "Masc"
                            elif word.feats[word.feats.find("Gender=")+len_of_gender : word.feats.find("Gender=")+len_of_gender+3] == "Fem":
                                gender = "Fem"
                            else:
                                gender = "Epi"

                        sentence_number, start_char_in_sentence, end_char_in_sentence = self.get_sentence_position(
                            sentence_starts,
                            word.parent.start_char,
                            word.parent.end_char
                        )

                        # store only the features we are interested in
                        # todo: start and end chars are using tokens, which is correct in most cases
                        new_am = AnnotatedMention(start_char=word.parent.start_char,
                                                  end_char=word.parent.end_char,
                                                  person=person,sentence=sent_no,
                                                  start_char_in_sentence=start_char_in_sentence,
                                                  end_char_in_sentence=end_char_in_sentence,
                                                  gender=gender)

                        self.annotated_mentions.append(new_am)



    def __repr__(self):
        repr_str = ""
        repr_str += str(self.sentence_bounds) + "\n\n"

        for am in self.annotated_mentions:
            repr_str += f"{am.start_char}, {am.end_char}, {am.sentence_number}, {am.start_char_in_sentence}, {am.end_char_in_sentence}, {am.gender}\n"

        return repr_str


