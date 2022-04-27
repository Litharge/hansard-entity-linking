# module containing functions for detecting where mentions are in passed text
# does not handle sentences, operates on raw characters

import re


def get_regex_span(spans, utt_span):
    spans_found = []

    for span in spans:
        for m in re.finditer(span, utt_span, re.IGNORECASE):
            print("here")
            spans_found.append(
                (m.start(0),
                 m.start(0) + len(span))
            )

    return spans_found


def get_hon_epicene_mentions(utt_span, sentence_starts):
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

    found_spans = get_regex_span(hon_spans, utt_span)

    return found_spans




def get_hon_masculine_mentions(utt_span, sentence_starts):
    hon_spans = [
        "the hon  gentleman",
        "the hon  and learned gentleman",
        "the right hon  gentleman",
        "the right hon  and learned gentleman"
    ]

    found_spans = get_regex_span(hon_spans, utt_span)

    return found_spans


def get_hon_feminine_mentions(utt_span, sentence_starts):
    hon_spans = [
        "the hon  lady",
        "the hon  and learned lady",
        "the right hon  lady",
        "the right hon  and learned lady"]

    found_spans = get_regex_span(hon_spans, utt_span)

    return found_spans

