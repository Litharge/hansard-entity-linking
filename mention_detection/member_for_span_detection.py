import re

from mention_detection.span_detection import get_regex_span


def get_member_for_spans(discourse_model, utt_span):
    prefixes = ["the hon  Member for ", "the Member for "]

    found_spans = []

    for mp in discourse_model.mp_list:
        search_terms = [prefix + mp.constituency for prefix in prefixes]

        print(search_terms)

        spans_with_associated_entity = [(span, mp) for span in get_regex_span(search_terms, utt_span)]

        found_spans.extend(spans_with_associated_entity)

    return found_spans


