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
    def __init__(self):
        self.annotated_mentions = []

        self.sentence_bounds = None
        self.sentence_starts = None

        # todo: this should be instance variable instead of arg

    # find all mentions that are adjacent, replace them with a single mention spanning their entirety in
    # self.annotated mentions, add all original mentions to the new mention's appos list
    def join_appositives(self, utt_span):
        # sort the AnnotatedMentions by start_char
        self.annotated_mentions.sort(key=lambda x: x.start_char)
        # go through each non-pronominal mention and look at the characters between it and the next mention
        # if the characters are of an allowed form, then add the mention to the appos chain and check the next between characters in the same way
        # else start a new appos candidate on the next mention
        for i in range(len(self.annotated_mentions) - 1):
            separating_span = utt_span[self.annotated_mentions[i].end_char:self.annotated_mentions[i+1].start_char]
            print("separating span", separating_span)

    # method that for a given utterance span utt_span and its corresponding stanza Document doc, adds mentions of
    # all relevant kinds to self.annotated_mentions
    def detect_mentions(self, nlp, utt_span, model_location, datetime_of_utterance):

        doc = nlp(utt_span)

        self.set_sentence_bounds(doc)

        self.sentence_starts = [item[0] for item in self.sentence_bounds]

        model = pickle.load(open(model_location, "rb"))

        sentence_starts = self.sentence_starts

        self.add_pronouns(doc, sentence_starts)

        hon_epicene_mentions = get_hon_epicene_mentions(utt_span, sentence_starts)
        self.add_am_list(hon_epicene_mentions, sentence_starts)

        hon_masculine_mentions = get_hon_masculine_mentions(utt_span, sentence_starts)
        self.add_am_list(hon_masculine_mentions, sentence_starts)

        hon_feminine_mentions = get_hon_feminine_mentions(utt_span, sentence_starts)
        self.add_am_list(hon_feminine_mentions, sentence_starts)

        speaker_mentions = get_speaker_mentions(utt_span)
        self.add_am_list(speaker_mentions, sentence_starts)

        deputy_speaker_masculine_mentions = get_deputy_speaker_masculine_mentions(utt_span)
        self.add_am_list(deputy_speaker_masculine_mentions, sentence_starts)

        deputy_speaker_feminine_ranges = get_deputy_speaker_feminine_mentions(utt_span)
        self.add_am_list(deputy_speaker_feminine_ranges, sentence_starts)

        member_for_mentions = get_member_for_spans(model, utt_span)
        self.add_am_list(member_for_mentions, sentence_starts)

        exact_offices_mentions = get_exact_office_spans(model, utt_span, datetime_of_utterance)
        self.add_am_list(exact_offices_mentions, sentence_starts)

        ministerial_class_mentions = get_ministerial_class_mentions(utt_span)
        self.add_am_list(ministerial_class_mentions, sentence_starts)

        exact_nominal_mentions = get_exact_nominal_mentions(model, utt_span)
        self.add_am_list(exact_nominal_mentions, sentence_starts)

        regular_secretary_mentions = get_regular_secretary_mentions(utt_span)
        self.add_am_list(regular_secretary_mentions, sentence_starts, allow_overlap=False)

        irregular_office_mentions = get_irregular_office_mentions(utt_span)
        self.add_am_list(irregular_office_mentions, sentence_starts, allow_overlap=False)


    # returns a tuple [start char index, end char index) for a sentence
    def set_sentence_bounds(self, doc):
        # dictionary containing sentence number as key and tuple of start and end char inclusive
        sentence_list = []

        for sentence in doc.sentences:
            sentence_list.append((sentence.tokens[0].start_char, sentence.tokens[-1].end_char))

        self.sentence_bounds = sentence_list

    # returns a tuple (sentence number, index of start character within sentence, index of end character within
    # sentence)
    def get_sentence_position(self, sentence_starts, start_char, end_char):
        sentence_number = bisect.bisect_right(sentence_starts, start_char) - 1

        start_char_in_sentence = start_char - sentence_starts[sentence_number]
        end_char_in_sentence = end_char - sentence_starts[sentence_number]

        return sentence_number, start_char_in_sentence, end_char_in_sentence

    def is_overlapping_with_existing(self, to_check):
        for item in self.annotated_mentions:
            if item.start_char <= to_check.start_char <= item.end_char or item.start_char <= to_check.end_char <= item.end_char:
                return True

        return False

    # todo this should only add irregular type and regular secretary type mentions if they do not overlap with existing mentions
    #  do this with a parameter, as we want first person pronouns to allow overlap for example in "my hon. friend"
    def add_am_list(self, mentions, sentence_starts, allow_overlap=True):
        for mention in mentions:
            if allow_overlap or not self.is_overlapping_with_existing(mention):
                mention.sentence_number, mention.start_char_in_sentence, mention.end_char_in_sentence = self.get_sentence_position(sentence_starts,
                                                                                                           mention.start_char,
                                                                                                           mention.end_char)
                self.annotated_mentions.append(mention)

    # todo: incorrectly adds interrogative "what", needs more processing, maybe look at person
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

                        if word.feats.find("Person=") != -1:
                            person = word.feats[word.feats.find("Person=")+len_of_person]
                            person = int(person)
                        else:
                            person = None

                        gender=None

                        print("word:", word.text, "gender:", word.feats[word.feats.find("Gender=")+len_of_gender : word.feats.find("Gender=")+len_of_gender+4])

                        if word.feats.find("Gender=") != -1:
                            if word.feats[word.feats.find("Gender=")+len_of_gender : word.feats.find("Gender=")+len_of_gender+4] == "Masc":
                                gender = "masculine"
                            elif word.feats[word.feats.find("Gender=")+len_of_gender : word.feats.find("Gender=")+len_of_gender+3] == "Fem":
                                gender = "feminine"
                            else:
                                gender = "epicene"

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
                                                  gender=gender,
                                                  role="pronominal_mention")

                        self.annotated_mentions.append(new_am)



    def __repr__(self):
        repr_str = ""
        repr_str += str(self.sentence_bounds) + "\n\n"

        for am in self.annotated_mentions:
            repr_str += f"{am.start_char}, {am.end_char}, {am.sentence_number}, {am.start_char_in_sentence}, {am.end_char_in_sentence}, {am.gender}\n"

        return repr_str


