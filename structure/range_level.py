import pickle

from lxml import etree

import stanza

from structure.utterance_level import Utterance

def transform_hon(to_transform):
    return to_transform.replace(" hon. ", " hon  ")


# class whose instance represents a whole xml document, containing an Utterance for each utterance
# class will iterate over each Utterance, calling its detect mentions method
# then it will iterate over each of the AnnotatedMentions in its list of Utterance, calling on the AnnotatedMention its resolution method
class WholeXMLAnnotation():
    def __init__(self, xml_location, start, end, model_location, datetime_of_utterance):
        self.datetime_of_utterance = datetime_of_utterance

        self.utterances = None

        self.utterers = {}

        self.set_all_mentions(xml_location, start, end, model_location, datetime_of_utterance)

        for key in self.utterances:
            self.utterances[key].join_appositives()

        self.ordered_mentions = {}
        self.order_mentions()

    def __str__(self):
        rep = ""
        for key in self.utterances:
            rep += f"==={key}===\n{self.utterers[key]}\n"
            for mention in self.utterances[key].annotated_mentions:
                rep += f"-\n{mention}\n-\n"

        return rep

    # iterate over an XML document stored in file specified by location, yielding an utterance span, from start to end
    # utterance id
    def get_utterance_spans(self, location, start, end):
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
                first_para = True
                for p in ch.getchildren():
                    if first_para:
                        first_para = False
                    else:
                        utterance_text += " "
                    utterance_text += "".join(p.itertext())

                utterance_text = transform_hon(utterance_text)

                if ch.get("person_id") is not None:
                    yield (utterance_text, ch.get("id"), ch.get("person_id"))
                else:
                    yield (utterance_text, ch.get("id"), ch.get("speakerid"))

            # end the loop when the end pid is found
            if ch.get("id") == end:
                break

    # return True if any of the offices in offices_to_check are secretaries of state
    def check_if_any_are_secretary(self, offices_to_check):
        for office in offices_to_check:
            if "Secretary of State" in office and not any(
                    x in office for x in ["Under-Secretary", "Under Secretary"]):
                return True

        return False

    # return True if any of the offices in offices_to_check are ministers of the crown
    def check_if_any_are_minister_of_the_crown(self, offices_to_check):
        for office in offices_to_check:
            if office[0:7] != "Member," and "PPS" not in office and "Secretary of State" not in office and ("minister" in office or "Minister" in office):
                return True

        return False

    # return True if any of the offices in offices_to_check are shadow offices
    def check_if_shadow(self, offices_to_check):
        for office in offices_to_check:
            if "shadow" in office or "Shadow" in office:
                return True

        return False

    # returns true if the mp is a speaker or deputy speaker, as these are the MPs who are addressed in Parliament
    def check_if_addressed(self, offices_to_check):
        for office in offices_to_check:
            if ("Speaker" in office or "speaker" in office) and "Speaker's" not in office and "speaker's" not in office:
                return True

        return False

    # method looks through the model and sets for each mp attributes describing shadow status, ministerial rankings
    # pickles the resulting extended model
    # returns string describing location of pickle of extended model
    def set_MP_statuses_at_time(self, model_location, at_datetime):
        model = pickle.load(open(model_location, "rb"))

        for i, mp in enumerate(model.mp_list):
            # list of all offices held at at_datetime
            offices_to_check = [key for key in mp.current_offices if at_datetime > mp.current_offices[key]]

            past_offices_to_check = [key for key in mp.past_offices if
                                 mp.past_offices[key][0] < at_datetime <= mp.past_offices[key][1]]

            offices_to_check.extend(past_offices_to_check)

            model.mp_list[i].is_secretary = self.check_if_any_are_secretary(offices_to_check)
            model.mp_list[i].is_minister_of_state = self.check_if_any_are_minister_of_the_crown(offices_to_check)
            model.mp_list[i].is_shadow = self.check_if_shadow(offices_to_check)
            model.mp_list[i].is_addressed = self.check_if_addressed(offices_to_check)

        return model

    # returns the MP from the model matching the passed id
    def get_MP_from_person_id(self, id, model):
        id_number = id.split("/")[-1]
        for mp in model.mp_list:
            id_of_mp = mp.url.split("mp/")[1]
            id_of_mp = id_of_mp.split("/")[0]

            if id_number == id_of_mp:
                return mp

        return None

    # sets all mentions and adds reference to utterer
    def set_all_mentions(self, xml_location, start, end, model_location, datetime_of_utterance):
        self.augmented_model = self.set_MP_statuses_at_time(model_location, datetime_of_utterance)

        self.utterances = {}

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')

        for utt_span, utterance_id, person_id in self.get_utterance_spans(xml_location, start, end):
            to_add = Utterance(utt_span)

            to_add.detect_mentions(nlp, self.augmented_model, datetime_of_utterance=datetime_of_utterance)

            self.utterances[utterance_id] = to_add

            self.utterers[utterance_id] = self.get_MP_from_person_id(person_id, self.augmented_model)

    # iterate over the items in self.utterances, then iterate over each of the items in the annotated_mentions of
    # these, calling the resolve() method of the AnnotatedMention and passing in contextual information to allow it
    # to perform entity linkin on itself
    def set_references(self):
        for utterance_key in self.utterances:
            for mention_index, mention in enumerate(self.utterances[utterance_key].annotated_mentions):
                # pass contextual information to the AnnotatedMention, so it can resolve itself
                mention.resolve(utterance_span=self.utterances[utterance_key].utt_span,
                                utterers=self.utterers,
                                utterance_id=utterance_key,
                                annotated_mentions=self.utterances[utterance_key].annotated_mentions,
                                mention_index=mention_index,
                                ordered_mentions=self.ordered_mentions[utterance_key],
                                model=self.augmented_model,
                                datetime_of_utterance=self.datetime_of_utterance)

    # sets a dictionary of lists of indexes corresponding to items in self.annotated_mentions in each Utterance
    # each value in the dict shall be a list like
    # a b c. d e f. g h. -> indexes of c b a f e d h g
    def order_mentions(self):
        for key in self.utterances:
            self.ordered_mentions[key] = self.utterances[key].order_mentions()


