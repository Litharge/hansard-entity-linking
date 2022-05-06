from mention_detection.span_detection import get_regex_span
from structure.annotated_mention import AnnotatedMention


def get_member_for_spans(discourse_model, utt_span):
    prefixes = ["the hon  Member for ", "the Member for "]

    found_spans = []

    for mp in discourse_model.mp_list:
        search_terms = [prefix + mp.constituency for prefix in prefixes]

        spans_with_associated_entity = [(span, mp) for span in get_regex_span(search_terms, utt_span)]

        found_spans.extend(spans_with_associated_entity)

    mentions = [
        AnnotatedMention(start_char=span[0][0], end_char=span[0][1], entity=span[1], role="member_for_mention") for
        span
        in
        found_spans]

    return mentions



