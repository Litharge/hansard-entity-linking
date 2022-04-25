# module to produce pronoun mentions

import stanza
from lxml import etree
import re

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
    sentence_dict = {}
    doc = nlp(utt_span)

    for sentence_no, sentence in enumerate(doc.sentences):
        sentence_dict[sentence_no] = (sentence.tokens[0].start_char, sentence.tokens[-1].end_char)

    return sentence_dict


def get_first_person_pronouns(utt_span):
    # bounds of the sections we are interested in, for "I've" this is the first char only
    first_person_pronoun_spans = {
        " I ": (1, 2), " I'": (1, 2), " me ": (1, 3), " myself ": (1, 7), " mine ": (1, 5), " my ": (1, 3),
        " I,": (1, 2), " me,": (1, 3), " myself,": (1, 7), " mine,": (1, 5), " my,": (1, 3),
        " I\.": (1, 2), " me\.": (1, 3), " myself\.": (1, 7), " mine\.": (1, 5), " my\.": (1, 3),
        "^I ": (1, 2), "^I'": (1, 2), "^me ": (1, 3), "^myself ": (1, 7), "^mine ": (1, 5), "^my ": (1, 3),
        "^I\.": (1, 2), "^me\.": (1, 3), "^myself\.": (1, 7), "^mine\.": (1, 5), "^my\.": (1, 3),
        " I$": (1, 2), " me$": (1, 3), " myself$": (1, 7), " mine$": (1, 5), " my$": (1, 3),
        "^I$": (1, 2), "^me$": (1, 3), "^myself$": (1, 7), "^mine$": (1, 5), "^my$": (1, 3)
    }

    spans_found = []

    for key in first_person_pronoun_spans:
        print(key)
        for m in re.finditer(key, utt_span, re.IGNORECASE):
            print("here")
            spans_found.append(
                (m.start(0) + first_person_pronoun_spans[key][0],
                m.start(0) + first_person_pronoun_spans[key][1])
            )

    return spans_found


# get mentions indexed by character [start, end)
def get_mentions_indexed_by_character(utt_span):
    get_first_person_pronouns(utt_span)


def get_mentions(location, start, end):
    # to put in get_sentences
    nlp = stanza.Pipeline(lang='en', processors='tokenize')

    for utt_span in get_utterance_spans(location, start, end):
        utt_span = transform_hon(utt_span)
        get_sentence_bounds(nlp, utt_span)

        # todo: function to get list of spans of quotations

        get_mentions_indexed_by_character(utt_span)




