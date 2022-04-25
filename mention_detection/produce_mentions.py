# module to produce pronoun mentions

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
    sentence_dict = {}
    doc = nlp(utt_span)

    for sentence_no, sentence in enumerate(doc.sentences):
        sentence_dict[sentence_no] = (sentence.tokens[0].start_char, sentence.tokens[-1].end_char)

    return sentence_dict


def get_mentions(location, start, end):
    # to put in get_sentences
    nlp = stanza.Pipeline(lang='en', processors='tokenize')

    for utt_span in get_utterance_spans(location, start, end):
        utt_span = transform_hon(utt_span)
        get_sentence_bounds(nlp, utt_span)


