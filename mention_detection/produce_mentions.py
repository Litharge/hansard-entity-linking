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
    def __init__(self, start_char=None, end_char=None, person=None, sentence=None):
        self.sentence_number = sentence
        self.person = person
        self.start_char_in_sentence = start_char
        self.end_char_in_sentence = end_char


# contains AnnotatedMention's
# has an id associated
class Mentions():
    def __init__(self, doc, sentence_bounds):
        self.annotated_mentions = []

        # store sentence bounds for conversions
        self.sentence_bounds = sentence_bounds

        len_of_number = len("Number=")
        len_of_person = len("Person=")

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

                        # store only the features we are interested in
                        # todo: start and end chars are using tokens, which is correct in most cases
                        new_am = AnnotatedMention(start_char=word.parent.start_char,
                                                  end_char=word.parent.end_char,
                                                  person=person,
                                                  sentence=sent_no)
                        self.annotated_mentions.append(new_am)



    def __repr__(self):
        repr_str = ""
        repr_str += str(self.sentence_bounds) + "\n\n"

        for am in self.annotated_mentions:
            repr_str += f"{am.sentence_number}, {am.start_char_in_sentence}, {am.end_char_in_sentence}\n"

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

