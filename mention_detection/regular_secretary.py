# recognise "the Home Secretary", "the Work, Retirement and Pensions Secretary" etc.

import re

from structure.annotated_mention import AnnotatedMention

def regex_get_start_end(span, utt_span):
    spans_found = []
    for m in re.finditer(span, utt_span):
        spans_found.append(
            (m.start(0),
             m.end(0))
        )

    return spans_found


def get_regular_secretary_mentions(utt_span):
    # list of triples ((span tuple), rank, shadow)
    spans_and_attributes = []

    regular_secretary_pattern = r"[Tt]he ([A-Z][a-z]*?)?(( and |, | )([A-Z][a-z]*?)*?)*? Secretary"

    spans = regex_get_start_end(regular_secretary_pattern, utt_span)

    #print(spans)

    mentions = [AnnotatedMention(start_char=span[0], end_char=span[1], is_shadow=False, rank="secretary_of_state", role="secretary_regular_mention") for span in spans]

    regular_shadow_secretary_pattern = r"[Tt]he [Ss]hadow ([A-Z][a-z]*)(( and |, | )([A-Z][a-z]*)*)*? Secretary"

    spans = regex_get_start_end(regular_shadow_secretary_pattern, utt_span)

    mentions.extend([AnnotatedMention(start_char=span[0], end_char=span[1], is_shadow=True, rank="secretary_of_state", role="secretary_regular_mention") for span in spans])

    return mentions
