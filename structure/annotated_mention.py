# module containing AnnotateMention, which is a class describing a single mention
# the class contains methods to perform entity linking and coreference resolution, given some provided contextual
# data

from fuzzywuzzy import process, fuzz


class AnnotatedMention():
    def __init__(self, start_char=None, end_char=None, sentence=None, start_char_in_sentence=None,
                                      end_char_in_sentence=None, person=None, gender=None, rank=None, is_shadow=None, is_addressed=None, role=None, entity=None):
        # syntactic info
        self.start_char = start_char
        self.end_char = end_char

        self.sentence_number = sentence
        self.start_char_in_sentence = start_char_in_sentence
        self.end_char_in_sentence = end_char_in_sentence

        self.person = person
        self.gender = gender

        self.rank = rank
        if self.rank == "secretary_of_state":
            self.is_secretary = True
        else:
            self.is_secretary = False

        if self.rank == "minister":
            self.is_minister_of_state = True
        else:
            self.is_minister_of_state = False

        self.is_shadow = is_shadow

        self.is_addressed = is_addressed

        self.role = role

        # semantic info
        self.entity = entity

        self.assoc_constituency = None

        # coreference info
        self.appos_chain = []
        self.is_appositive = False


    def get_associated_constituency(self):
        if self.entity is not None:
            assoc_constituency = self.entity.constituency
        else:
            assoc_constituency = None

        return assoc_constituency

    def member_for_mention(self, context):
        pass


    # return the string of the single closest match, using search_term on the list to_search
    def get_closest_match(self, search_term, to_search):
        # fuzz.ratio is superior to fuzz.partial ratio, as otherwise the words common to the different offices
        # dominate, rather than the words that discriminate them
        result = process.extract(search_term, to_search, scorer=fuzz.ratio)

        if result is not None:
            # return text only
            return result[0][0]
        else:
            return None


    # return a dictionary with items of the form office:mp, where the offices are held at the given datetime as
    # described in the model. If matching_attrib contains strings, then the attributes of the mention and the
    # mp in the model with those names must match
    def get_office_mp_dict_at_time(self, model, datetime, matching_attrib=[]):
        office_mp_dict = {}

        for mp in model.mp_list:
            # first add from the past offices, which requires checking both the start and end dates
            for office in mp.past_offices:
                if mp.past_offices[office][0] < datetime <= mp.past_offices[office][1]:
                    outer_continue = False

                    for attrib in matching_attrib:
                        try:
                            if getattr(self, attrib) != getattr(mp, attrib):
                                # set outer_continue to continue the mp iteration loop and avoid adding the mp to the
                                # dictionary if there is some attribute mismatch
                                outer_continue = True
                        except AttributeError as e:
                            raise AttributeError(
                                "Attribute name not found, check that the attribute name is one of those for "
                                "an object attribute declared in the constructor")

                    if outer_continue:
                        continue

                    office_mp_dict[office] = mp

            # now add from the current offices, which requires only checking the start date
            for office in mp.current_offices:
                if mp.current_offices[office] < datetime:
                    outer_continue = False
                    for attrib in matching_attrib:
                        try:
                            if getattr(self, attrib) != getattr(mp, attrib):
                                # set outer_continue to continue the mp iteration loop and avoid adding the mp to the
                                # dictionary if there is some attribute mismatch
                                outer_continue = True
                        except AttributeError as e:
                            raise AttributeError(
                                "Attribute name not found, check that the attribute name is one of those for "
                                "an object attribute declared in the constructor")

                    if outer_continue:
                        continue

                    office_mp_dict[office] = mp

        return office_mp_dict

    # assign self.entity based on the context in the case of the mention being an irregular office e.g. "the Chancellor"
    def irregular_office_mention(self, context):
        model = context["model"]
        utt_span = context["utterance_span"]
        datetime_of_utterance = context["datetime_of_utterance"]

        text = utt_span[self.start_char:self.end_char]

        office_mp_dict = self.get_office_mp_dict_at_time(model, datetime_of_utterance)

        key = self.get_closest_match(text, list(office_mp_dict.keys()))

        self.entity = office_mp_dict[key]

    # assign self.entity based on the context in the case of the mention being a speaker mention
    def speaker_mention(self, context):
        model = context["model"]
        datetime_of_utterance = context["datetime_of_utterance"]

        office_mp_dict = self.get_office_mp_dict_at_time(model, datetime_of_utterance,
                                                         matching_attrib=["is_addressed"])

        key = self.get_closest_match("Speaker", list(office_mp_dict.keys()))

        self.entity = office_mp_dict[key]


    # this method could be written to match exact nominal mentions based on the context
    def exact_nominal_mention(self, context):
        pass

    # self.entity was actually assigned in the mention detection stage in the case of exact office mentions, so this
    # method can remain empty
    def exact_office_mention(self, context):
        pass

    # assign self.entity based on the context in the case of the mention being a regular secretary mention e.g.
    # "the Home Secretary", "the Foreign Secretary"
    def secretary_regular_mention(self, context):
        model = context["model"]
        utt_span = context["utterance_span"]
        datetime_of_utterance = context["datetime_of_utterance"]

        text = utt_span[self.start_char:self.end_char]
        # remove the leading "the " and the trailing " secretary", otherwise the secretary component is prioritised
        # with the default (best performing) scorer and does not produce useful results for short queries
        text_important_only = text[4:-10]

        office_mp_dict = self.get_office_mp_dict_at_time(model, datetime_of_utterance, matching_attrib=["is_secretary", "is_shadow"])

        # remove leading "the Secretary of State for" as the query may match with characters in this part, favouring
        # shorter office titles, e.g. "Home" -> "The Secretary of State for Wales" rather than
        # "The Secretary of State for the Home Department", because there are a higher proportion of characters
        useful_only = {}
        for key in office_mp_dict:
            if "The Secretary of State for " in key:
                new_key = key.split("The Secretary of State for ")[1]

                useful_only[new_key] = office_mp_dict[key]


        key = self.get_closest_match(text_important_only, list(useful_only.keys()))

        self.entity = useful_only[key]

    # assign self.entity based on the context in the case of the mention being a minister class mention, e.g.
    # "the Secretary of State", "the shadow Minister"
    def minister_class_mention(self, context):
        utterers = context["utterers"]
        utterance_id = context["utterance_id"]

        self.find_nearest_previous_utterer_matching_attributes(utterers, utterance_id, ["is_secretary", "is_minister_of_state", "is_shadow"])

    # this method could be written to match deputy speaker mentions based on the context
    def deputy_speaker_mention(self, context):
        pass

    # returns the last MP in utterers occurring before the utterance_id with the matching attribs_to_check, e.g.
    # "is_secretary", based on the model
    def find_nearest_previous_utterer_matching_attributes(self, utterers, utterance_id, attribs_to_check=None):
        # since python 3.7 dictionaries maintain insertion order
        utterers_keys = list(utterers.keys())
        utterance_position = utterers_keys.index(utterance_id)

        utterer_to_check_index = utterance_position
        while True:
            utterer_to_check_index -= 1

            # if the utterer index goes negative, then all utterers have been iterated through with no match being
            # found, so leave self.entity as None
            if utterer_to_check_index < 0:
                self.entity = None
                break

            self.entity = utterers[utterers_keys[utterer_to_check_index]]

            # if entity not in model, keep going
            if self.entity is None:
                continue

            match_on_all_attribs = True
            for attrib in attribs_to_check:
                try:
                    if getattr(self.entity, attrib) != getattr(self, attrib):
                        match_on_all_attribs = False
                        break
                except AttributeError as e:
                    raise AttributeError("Attribute name not found, check that the attribute name is one of those for "
                                         "an object attribute declared in the constructor")

            # if entity is a match then break the loop, as the correct entity has been assigned to self.entity
            if match_on_all_attribs:
                break

    # assign self.entity based on the context in the case of the mention being a minister class mention, e.g.
    # "the Secretary of State", "the shadow Minister"
    def hon_mention(self, context):
        utterers = context["utterers"]
        utterance_id = context["utterance_id"]

        # this mention refers to someone other than the addressee
        self.is_addressed = False
        self.find_nearest_previous_utterer_matching_attributes(utterers, utterance_id, attribs_to_check=["is_addressed"])

    # assign self.entity based on the context in the case of the mention being a minister class mention
    # simply assign the utterer to self.entity
    def pronominal_mention_1(self, context):
        utterers = context["utterers"]
        utterance_id = context["utterance_id"]
        self.entity = utterers[utterance_id]

    # this method could be written to match second person pronoun mentions e.g. "you", "your", based on the context
    def pronominal_mention_2(self, context):
        pass

    # return true if the mp's role is not in the disallowed class
    # todo: rename to relate to role
    def mention_roles_match(self, candidate_antecedent, disallowed_roles=[]):
        if candidate_antecedent.role not in disallowed_roles:
            return True

        return False

    # assign self.entity based on the context in the case of the mention being a third person singular pronoun e.g.
    # "he", "his"
    def pronominal_mention_3(self, context):
        annotated_mentions = context["annotated_mentions"]
        ordered_mentions = context["ordered_mentions"]

        break_i = False
        # iterate over sentences in reverse
        for i in range(self.sentence_number, -1, -1):
            # iterate mentions left to right as in Raghunathan et al. (2010)
            for j in range(len(ordered_mentions[i])):
                # if the candidate antecedent matches then the entity can be set to match that of the antecedent and the loop can break
                if self.mention_roles_match(annotated_mentions[ordered_mentions[i][j]],
                                            disallowed_roles=["pronominal_mention"]):
                    self.entity = annotated_mentions[ordered_mentions[i][j]].entity
                    break_i = True
                    break
            if break_i:
                break

    # this method could be written to assign
    def pronominal_mention_other(self, context):
        pass

    def pronominal_mention(self, context):
        # now call a specific method based on the person of the pronoun
        try:
            getattr(self, f"{self.role}_{self.person}")(context)
        except AttributeError as e:
            raise AttributeError("Role attribute as method name not found, check that the role is set correctly or"
                                 "that there is a method corresponding to the role")


    # assign an associated entity
    def resolve(self, **context):
        # if the entity was already set in the mention detection stage due to 1 to 1 mapping, there is no work to be
        # done
        if self.entity is not None:
            return

        # call correct method based on role of mention
        # using getattr() is safer than using exec()
        # the packed dictionary is passed in as the different possible methods need different items, the needed items
        # are then retrieved from the dictionary in the relevant method
        try:
            getattr(self, self.role)(context)
        except AttributeError as e:
            raise AttributeError("Role attribute as method name not found, check that the role is set correctly or"
                                 "that there is a method corresponding to the role")

    def __str__(self):
        return f"{self.start_char}, {self.end_char}\n" \
               f"{self.sentence_number}, {self.start_char_in_sentence}, {self.end_char_in_sentence}\n" \
               f"{self.person}, {self.gender}\n" \
               f"{self.rank}, shadow? {self.is_shadow}\n" \
               f"{self.role}\n" \
               f"constituency of associated MP: {self.get_associated_constituency()}"
