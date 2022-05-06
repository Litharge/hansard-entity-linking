from mention_detection.span_detection import get_regex_span

from structure.annotated_mention import AnnotatedMention

def get_irregular_office_mentions(utt_span):
    # bounds of the sections we are interested in, for "I've" this is the first char only
    irregular_spans = [
        "the Paymaster General",
        "the Prime Minister",
        "the Deputy Prime Minister",
        "the Chancellor",
        "the Lord Chancellor",
        "the Leader of the Opposition"
    ]

    spans = get_regex_span(irregular_spans, utt_span)

    mentions = [AnnotatedMention(start_char=span[0], end_char=span[1], role="irregular_office_mention") for span in spans]

    return mentions