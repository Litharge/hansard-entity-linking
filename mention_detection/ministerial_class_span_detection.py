# recognise "the Secretary of State", "the Minister" etc

import re

from mention_detection.annotated_mention import AnnotatedMention

def regex_get_start_end(span, utt_span):
    spans_found = []
    for m in re.finditer(span, utt_span, re.IGNORECASE):
        #print("here")
        spans_found.append(
            (m.start(0),
             m.start(0) + len(span))
        )

    return spans_found


def get_ministerial_class_mentions(utt_span):
    # list of triples ((span tuple), rank, shadow)
    spans_and_attributes = []

    to_search_and_attributes = [
        ("the Secretary of State", "secretary_of_state", False),
        ("the Minister", "minister", False),
        ("the Under-Secretary", "under_secretary", False),
        ("the shadow Secretary of State", "secretary_of_state", True),
        ("the shadow Minister", "minister", True),
    ]

    for item in to_search_and_attributes:
        spans = regex_get_start_end(item[0], utt_span)
        # todo: actually return a span object, which is then used by method in utterance level
        spans_with_attributes = [AnnotatedMention(start_char=span[0], end_char=span[1], rank=item[1], is_shadow=item[2], role="minister_class_mention") for span in spans]

        spans_and_attributes.extend(spans_with_attributes)

    return spans_and_attributes
