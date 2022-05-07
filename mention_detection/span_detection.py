# module containing functions for detecting where mentions are in passed text
# does not handle sentences, operates on raw characters

import re

from structure.annotated_mention import AnnotatedMention


def get_regex_span(spans, utt_span):
    spans_found = []

    for span in spans:
        for m in re.finditer(span, utt_span, re.IGNORECASE):
            spans_found.append(
                (m.start(0),
                 m.start(0) + len(span))
            )

    return spans_found


def get_hon_epicene_mentions(utt_span, sentence_starts):
    # bounds of the sections we are interested in, for "I've" this is the first char only
    # todo: "the hon  member" can form part of larger mention incorrectly
    hon_spans = [
        "my hon  friend",
        "my hon  and learned friend",
        "my right hon  friend",
        "my right hon  and learned friend",
        #"the hon  member",
        #"the hon  and learned member",
        "the right hon  member",
        "the right hon  and learned member",
    ]

    found_spans = get_regex_span(hon_spans, utt_span)

    mentions = [AnnotatedMention(start_char=span[0], end_char=span[1], gender="epicene", role="hon_mention") for span in found_spans]

    return mentions




def get_hon_masculine_mentions(utt_span, sentence_starts):
    hon_spans = [
        "the hon  gentleman",
        "the hon  and learned gentleman",
        "the right hon  gentleman",
        "the right hon  and learned gentleman"
    ]

    found_spans = get_regex_span(hon_spans, utt_span)

    mentions = [AnnotatedMention(start_char=span[0], end_char=span[1], gender="masculine", role="hon_mention") for span in
                found_spans]

    return mentions


def get_hon_feminine_mentions(utt_span, sentence_starts):
    hon_spans = [
        "the hon  lady",
        "the hon  and learned lady",
        "the right hon  lady",
        "the right hon  and learned lady"
    ]

    found_spans = get_regex_span(hon_spans, utt_span)

    mentions = [AnnotatedMention(start_char=span[0], end_char=span[1], gender="feminine", role="hon_mention") for span
                in
                found_spans]

    return mentions


# no need to distinguish gender of speaker, there is only one at a time
def get_speaker_mentions(utt_span):
    hon_spans = [
        "Mr Speaker",
        "Madam Speaker"
    ]

    found_spans = get_regex_span(hon_spans, utt_span)

    mentions = [AnnotatedMention(start_char=span[0], end_char=span[1], is_addressed=True, gender=None, role="speaker_mention") for span
                in
                found_spans]

    return mentions


def get_deputy_speaker_masculine_mentions(utt_span):
    hon_spans = [
        "Mr Deputy Speaker"
    ]

    found_spans = get_regex_span(hon_spans, utt_span)

    mentions = [AnnotatedMention(start_char=span[0], end_char=span[1], gender="masculine", role="deputy_speaker_mention") for span
                in
                found_spans]

    return mentions

def get_deputy_speaker_feminine_mentions(utt_span):
    hon_spans = [
        "Madam Deputy Speaker"
    ]

    found_spans = get_regex_span(hon_spans, utt_span)

    mentions = [
        AnnotatedMention(start_char=span[0], end_char=span[1], gender="feminine", role="deputy_speaker_mention") for
        span
        in
        found_spans]

    return mentions

