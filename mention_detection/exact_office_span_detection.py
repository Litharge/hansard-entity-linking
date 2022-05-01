import re

from mention_detection.span_detection import get_regex_span

from discourse_model.model_from_list import MPList


def prepend_definite_article(to_prepend):
    with_article = []

    for item in to_prepend:
        if item[0:3] != "The" and item[0:3] != "the":
            with_article.append("The " + item)
        else:
            with_article.append(item)

    return with_article


def get_exact_office_spans(discourse_model: MPList, utt_span, datetime):
    found_spans = []

    for mp in discourse_model.mp_list:
        #for key in mp.current_offices:
        #    print(key)
        # look at current offices
        search_terms = [key for key in mp.current_offices if datetime > mp.current_offices[key]]

        search_terms_past = [key for key in mp.past_offices if mp.past_offices[key][0] < datetime <= mp.past_offices[key][1]]

        search_terms.extend(search_terms_past)

        search_terms = prepend_definite_article(search_terms)

        spans_with_associated_entity = [span for span in get_regex_span(search_terms, utt_span)]

        found_spans.extend(spans_with_associated_entity)

    return found_spans
