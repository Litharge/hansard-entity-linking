# module to produce pronoun mentions

import re
import bisect

import stanza
from lxml import etree


# iterate through [desired range] of [a given xml file]
# first determine sentence bounds
# will need to replace "hon." with "hon " as stanza is unable to parse abbreviation periods


def transform_hon(to_transform):
    return to_transform.replace(" hon. ", " hon  ")


def get_utterance_spans(location, start, end):
    tree = etree.parse(location)

    root = tree.getroot()

    seen_start = False

    for ch in root.getchildren():
        # skip the loop until the start pid is found
        if not seen_start and ch.get("id") != start:
            continue
        else:
            seen_start = True

        utterance_text = ""
        if ch.tag == "speech" and not ch.get("nospeaker") == "true":
            for p in ch.getchildren():
                utterance_text += "".join(p.itertext())

            utterance_text = transform_hon(utterance_text)

            yield utterance_text

        # end the loop when the end pid is found
        if ch.get("id") == end:
            break


def get_sentence_bounds(doc):
    # dictionary containing sentence number as key and tuple of start and end char inclusive
    sentence_list = []


    for sentence in doc.sentences:
        sentence_list.append((sentence.tokens[0].start_char, sentence.tokens[-1].end_char))

    return sentence_list



# instances represent mentions in sentences
# can take on additional data e.g. linking to a cluster
class AnnotatedMention():
    def __init__(self, start_char=None, end_char=None, sentence=None, start_char_in_sentence=None,
                                      end_char_in_sentence=None, person=None, gender=None):
        self.start_char = start_char
        self.end_char = end_char

        self.sentence_number = sentence
        self.start_char_in_sentence = start_char_in_sentence
        self.end_char_in_sentence = end_char_in_sentence
        self.person = person
        # todo: these actually assign overall character


        self.gender = gender


# contains AnnotatedMention's
# has an id associated
class Mentions():
    def __init__(self, doc, utt_span, sentence_bounds):
        self.annotated_mentions = []

        # todo: this should be instance variable instead of arg
        sentence_starts = [item[0] for item in sentence_bounds]

        # store sentence bounds for conversions
        self.sentence_bounds = sentence_bounds

        self.add_pronouns(doc, sentence_starts)


        self.add_hon_epicene_mentions(utt_span, sentence_starts)
        self.add_hon_masculine_mentions(utt_span, sentence_starts)
        self.add_hon_feminine_mentions(utt_span, sentence_starts)


    def get_regex_span(self, spans, utt_span):
        spans_found = []

        for span in spans:
            for m in re.finditer(span, utt_span, re.IGNORECASE):
                print("here")
                spans_found.append(
                    (m.start(0),
                     m.start(0) + len(span))
                )

        return spans_found

    def get_sentence_position(self, sentence_starts, start_char, end_char):
        sentence_number = bisect.bisect_right(sentence_starts, start_char) - 1

        start_char_in_sentence = start_char - sentence_starts[sentence_number]
        end_char_in_sentence = end_char - sentence_starts[sentence_number]

        return sentence_number, start_char_in_sentence, end_char_in_sentence

    # using a list of found span tuples, add AnnotatedMentions to self.annotated_mentions
    def add_am(self, gender, found_spans, sentence_starts):
        for mention in found_spans:
            sentence_number, start_char_in_sentence, end_char_in_sentence = self.get_sentence_position(sentence_starts, mention[0], mention[1])

            new_am = AnnotatedMention(start_char=mention[0],
                                      end_char=mention[1],
                                      sentence=sentence_number,
                                      start_char_in_sentence=start_char_in_sentence,
                                      end_char_in_sentence=end_char_in_sentence,
                                      person=None,
                                      gender=gender)

            self.annotated_mentions.append(new_am)



    def add_hon_epicene_mentions(self, utt_span, sentence_starts):
        # bounds of the sections we are interested in, for "I've" this is the first char only
        hon_spans = [
            "my hon  friend",
            "my hon  and learned friend",
            "my right hon  friend",
            "my right hon  and learned friend",
            "the hon  member",
            "the hon  and learned member",
            "the right hon  member",
            "the right hon  and learned member",
        ]

        found_spans = self.get_regex_span(hon_spans, utt_span)

        self.add_am("epicene", found_spans, sentence_starts)


    def add_hon_masculine_mentions(self, utt_span, sentence_starts):
        hon_spans = [
        "the hon  gentleman",
        "the hon  and learned gentleman",
        "the right hon  gentleman",
        "the right hon  and learned gentleman"
        ]

        found_spans = self.get_regex_span(hon_spans, utt_span)

        self.add_am("masculine", found_spans, sentence_starts)

    def add_hon_feminine_mentions(self, utt_span, sentence_starts):
        hon_spans = [
        "the hon  lady",
        "the hon  and learned lady",
        "the right hon  lady",
        "the right hon  and learned lady"]

        found_spans = self.get_regex_span(hon_spans, utt_span)

        self.add_am("feminine", found_spans, sentence_starts)


    def add_pronouns(self, doc, sentence_starts):
        len_of_number = len("Number=")
        len_of_person = len("Person=")
        len_of_gender = len("Gender=")

        # add pronouns to annotated_mentions
        for sent_no, sentence in enumerate(doc.sentences):
            for word in sentence.words:

                if word.feats is not None:
                    # if the word is a pronoun, look at the feats string to determine if the pronoun is singular
                    if word.upos == "PRON" and word.feats[word.feats.find("Number=")+len_of_number : word.feats.find("Number=")+len_of_number+4]:
                        # filter out neuter and epicene pronouns, feats does not contain information to discriminate this
                        if word.text.lower() in ["it", "itself", "its", "they", "them", "themselves", "theirs", "their"]:
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
                            sentence_starts, word.parent.start_char, word.parent.end_char)

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

"""
def get_mentions(location, start, end):
    # to put in get_sentences
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')

    doc = nlp(utt_span)

    # goes through each entire utterance span,
    for utt_span in get_utterance_spans(location, start, end):
        utt_span = transform_hon(utt_span)

        sentence_bounds = get_sentence_bounds(doc)

        # todo: function to get list of spans of quotations

        #mentions = get_first_person_pronouns(utt_span)

        sentence_mentions = Mentions(doc, sentence_bounds)
"""

