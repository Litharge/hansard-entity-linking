from lxml import etree

import stanza

from mention_detection.utterance_level import Mentions

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

            yield (utterance_text, ch.get("id"), ch.get("person_id"))

        # end the loop when the end pid is found
        if ch.get("id") == end:
            break


# class whose instance represents a whole xml document, containing a Mentions for each utterance
# class will iterate over each Mentions, calling its detect mentions method
# then it will iterate over each of the AnnotatedMentions in its list of Mentions, calling on the AnnotatedMention its resolution method
class WholeXMLAnnotation():
    def __init__(self, xml_location, start, end, model_location, datetime_of_utterance):
        self.utterance_mentions = {}

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')

        for utt_span, utterance_id, person_id in get_utterance_spans(xml_location, start, end):
            print("\n\nutterance id: ", utterance_id)
            to_add = Mentions()

            utt_span = transform_hon(utt_span)

            to_add.detect_mentions(nlp, utt_span, model_location, datetime_of_utterance=datetime_of_utterance)

            self.utterance_mentions[utterance_id] = to_add

    def __str__(self):
        rep = ""
        for key in self.utterance_mentions:
            rep += f"==={key}===\n"
            for mention in self.utterance_mentions[key].annotated_mentions:
                rep += f"-\n{mention}\n-\n"

        return rep