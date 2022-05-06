import pickle

from lxml import etree

import stanza

from structure.utterance_level import Mentions

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

            if ch.get("person_id") is not None:
                yield (utterance_text, ch.get("id"), ch.get("person_id"))
            else:
                yield (utterance_text, ch.get("id"), ch.get("speakerid"))

        # end the loop when the end pid is found
        if ch.get("id") == end:
            break


# class whose instance represents a whole xml document, containing a Mentions for each utterance
# class will iterate over each Mentions, calling its detect mentions method
# then it will iterate over each of the AnnotatedMentions in its list of Mentions, calling on the AnnotatedMention its resolution method
class WholeXMLAnnotation():
    def check_if_any_are_secretary(self, offices_to_check):
        for office in offices_to_check:
            if "Secretary of State" in office and not any(
                    x in office for x in ["Under-Secretary", "Under Secretary"]):
                return True

        return False

    def check_if_any_are_minister_of_the_crown(self, offices_to_check):
        for office in offices_to_check:
            if office[0:7] != "Member," and "PPS" not in office and "Secretary of State" not in office and ("minister" in office or "Minister" in office):
                return True

        return False

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

        new_location = f"{model_location[:-2]}_{at_datetime.strftime('%Y_%m_%d')}.p"
        pickle.dump(model, open(new_location, "wb"))

        for mp in model.mp_list:
            print(mp)
            print("is_secretary:", mp.is_secretary)
            print("is_minister_of_state:", mp.is_minister_of_state)
            print("is_shadow:", mp.is_shadow)
            print("is_addressed", mp.is_addressed)

        # todo: ultimately this should just return model, but need to refactor mention detection stuff first
        return model, new_location

    # looks in the model for a matching mp based on their id
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
        self.augmented_model, self.augmented_model_location = self.set_MP_statuses_at_time(model_location, datetime_of_utterance)

        self.utterance_mentions = {}

        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')

        for utt_span, utterance_id, person_id in get_utterance_spans(xml_location, start, end):
            print("utt_span", utt_span)
            print("\n\nutterance id: ", utterance_id)
            to_add = Mentions()

            utt_span = transform_hon(utt_span)

            to_add.detect_mentions(nlp, utt_span, self.augmented_model_location, datetime_of_utterance=datetime_of_utterance)

            self.utterance_mentions[utterance_id] = to_add

            self.utterers[utterance_id] = self.get_MP_from_person_id(person_id, self.augmented_model)

    def set_references(self):
        for utterance_key in self.utterance_mentions:
            for mention_index, mention in enumerate(self.utterance_mentions[utterance_key].annotated_mentions):
                # pass contextual information to the mention so it can resolve itself
                # the relevant information is:
                # * who the utterers are
                # * which utterance the mention is in
                # * the mentions within that utterance only
                # * the index that this mention is within those utterances
                mention.resolve(#utterance_span=self.utterance_mentions[utterance_key].utt_span,
                                utterers=self.utterers,
                                utterance_id=utterance_key,
                                annotated_mentions=self.utterance_mentions[utterance_key].annotated_mentions,
                                mention_index=mention_index,
                                ordered_mentions=self.ordered_mentions[utterance_key],
                                model=self.augmented_model)

    # sets a dictionary of lists of indexes corresponding to items in self.annotated_mentions in each Mentions
    # each value in the dict shall be a list like
    # a b c. d e f. g h. -> indexes of c b a f e d h g
    def order_mentions(self):
        print("in order_mentions")
        for key in self.utterance_mentions:
            self.ordered_mentions[key] = self.utterance_mentions[key].order_mentions()

    def __init__(self, xml_location, start, end, model_location, datetime_of_utterance):
        self.augmented_model_location = None

        self.utterance_mentions = None

        self.utterers = {}

        self.set_all_mentions(xml_location, start, end, model_location, datetime_of_utterance)

        print("---")
        #print("utterance_mentions:", self.utterance_mentions['uk.org.publicwhip/debate/2020-06-15a.503.6'])
        print("---")
        for key in self.utterance_mentions:
            self.utterance_mentions[key].join_appositives()

        self.ordered_mentions = {}
        self.order_mentions()





    def __str__(self):
        rep = ""
        for key in self.utterance_mentions:
            rep += f"==={key}===\n{self.utterers[key]}\n"
            for mention in self.utterance_mentions[key].annotated_mentions:
                rep += f"-\n{mention}\n-\n"

        return rep
