import re

from discourse_model.model_from_list import MPList

from structure.annotated_mention import AnnotatedMention


def regex_get_start_end(span, utt_span):
    spans_found = []
    for m in re.finditer(span, utt_span):
        spans_found.append(
            (m.start(0),
             m.end(0))
        )

    return spans_found


def get_exact_nominal_mentions(discourse_model: MPList, utt_span):
    found_spans = []

    for mp in discourse_model.mp_list:
        exact_nominal = f"\(?{mp.first_name} {mp.last_name}\)?"

        spans_with_associated_entity = regex_get_start_end(exact_nominal, utt_span)

        found_spans.extend([AnnotatedMention(start_char=item[0], end_char=item[1], entity=mp, role="exact_nominal_mention") for item in spans_with_associated_entity])

    return found_spans
