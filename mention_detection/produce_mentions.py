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


def get_sentence_bounds(nlp: stanza.Pipeline, utt_span: str):
    # dictionary containing sentence number as key and tuple of start and end char inclusive
    sentence_list = []
    doc = nlp(utt_span)

    for sentence in doc.sentences:
        sentence_list.append((sentence.tokens[0].start_char, sentence.tokens[-1].end_char))

    return sentence_list


def get_regex_mention_spans(utt_span, regex):
    spans_found = []

    for key in regex:
        print(key)
        for m in re.finditer(key, utt_span, re.IGNORECASE):
            print("here")
            spans_found.append(
                (m.start(0) + regex[key][0],
                m.start(0) + regex[key][1])
            )

    return spans_found


# get mentions indexed by character [start, end)
def get_first_person_pronouns(utt_span):
    # bounds of the sections we are interested in, e.g. for "I've" this is the first char only
    first_person_pronoun_spans = {
        " I ": (1, 2), " me ": (1, 3), " myself ": (1, 7), " mine ": (1, 5), " my ": (1, 3),
        " I\W": (1, 2), " me\W": (1, 3), " myself\W": (1, 7), " mine\W": (1, 5), " my\W": (1, 3),
        "^I ": (0, 1), "^me ": (0, 2), "^myself ": (0, 6), "^mine ": (0, 4), "^my ": (0, 2),
        "^I\W": (0, 1), "^me\W": (0, 2), "^myself\W": (0, 6), "^mine\W": (0, 4), "^my\W": (1, 3),
        " I$": (1, 2), " me$": (1, 3), " myself$": (1, 7), " mine$": (1, 5), " my$": (0, 2),
        "^I$": (0, 1), "^me$": (0, 2), "^myself$": (0, 6), "^mine$": (0, 4), "^my$": (0, 2)
    }

    first_person_pronoun_spans = get_regex_mention_spans(utt_span, first_person_pronoun_spans)

    return first_person_pronoun_spans


# instances represent mentions in sentences
# can take on additional data e.g. linking to a cluster
class AnnotatedMention():
    def __init__(self, sentence_starts, sentence_bounds, mention):
        # find which sentence the mention begins in based on the start character index
        # todo: this can be sped up by a modified linear search, although may be less readable
        self.sentence_number = bisect.bisect_right(sentence_starts, mention[0]) - 1

        self.start_char_in_sentence = mention[0] - sentence_starts[self.sentence_number]
        self.end_char_in_sentence = mention[1] - sentence_starts[self.sentence_number]


# contains AnnotatedMention's
# has an id associated
class Mentions():
    def __init__(self, mentions, sentence_bounds):
        self.annotated_mentions = []

        self.sentence_bounds = sentence_bounds

        # generate sentence starts for binary search once, so that each AnnotatedMention doesnt have to generate it
        sentence_starts = [item[0] for item in sentence_bounds]

        for m in mentions:
            am = AnnotatedMention(sentence_starts, sentence_bounds, m)
            self.annotated_mentions.append(am)

    def __repr__(self):
        repr_str = ""
        repr_str += str(self.sentence_bounds) + "\n\n"

        for am in self.annotated_mentions:
            repr_str += f"{am.sentence_number}, {am.start_char_in_sentence}, {am.end_char_in_sentence}\n"

        return repr_str


def get_mentions(location, start, end):
    # to put in get_sentences
    nlp = stanza.Pipeline(lang='en', processors='tokenize')

    # goes through each entire utterance span,
    for utt_span in get_utterance_spans(location, start, end):
        utt_span = transform_hon(utt_span)
        sentence_bounds = get_sentence_bounds(nlp, utt_span)

        # todo: function to get list of spans of quotations

        mentions = get_first_person_pronouns(utt_span)

        sentence_mentions = Mentions(mentions, sentence_bounds)


