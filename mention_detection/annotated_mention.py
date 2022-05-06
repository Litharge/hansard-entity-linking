# todo: place call to get_matching_antecedent() in here, this will be a function in a coreference subpackage that
#  takes in params for what type of mention to look for then return the matching chain id
#  MAYBE place AnnotatedMention in the coreference package, then Mentions is seen as detecting the mentions, ready
#  for them to perform coref resolution
# instances represent mentions in sentences
# can take on additional data e.g. linking to a cluster
class AnnotatedMention():
    def __init__(self, start_char=None, end_char=None, sentence=None, start_char_in_sentence=None,
                                      end_char_in_sentence=None, person=None, gender=None, rank=None, is_shadow=None, role=None, entity=None):
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

        self.role = role

        self.entity = entity

        self.assoc_constituency = None

        self.appos_chain = []
        self.is_appositive = False


    def get_associated_constituency(self):
        if self.entity is not None:
            assoc_constituency = self.entity.constituency
        else:
            assoc_constituency = None

        return assoc_constituency

    def member_for_mention(self, context):
        print("in member_for_mention")
    def irregular_office_mention(self, context):
        pass
    def speaker_mention(self, context):
        pass
    def exact_nominal_mention(self, context):
        pass
    def exact_office_mention(self, context):
        pass
    def secretary_regular_mention(self, context):
        pass
    def minister_class_mention(self, context):
        utterers = context["utterers"]
        utterance_id = context["utterance_id"]
        model = context["model"]

        self.find_nearest_previous_utterer_matching_attributes(utterers, utterance_id, model, ["is_secretary", "is_minister_of_state", "is_shadow"])


    def deputy_speaker_mention(self, context):
        pass
    def find_nearest_previous_utterer_matching_attributes(self, utterers, utterance_id, model, attribs_to_check=None):
        # since python 3.7 dictionaries maintain insertion order
        utterers_keys = list(utterers.keys())
        utterance_position = utterers_keys.index(utterance_id)
        print("utterance pos:", utterance_position)

        # simply gets previous utterer
        # todo: improve this by using own attributes and matching against them
        utterer_to_check_index = utterance_position
        while True:
            utterer_to_check_index -= 1
            print("utterer_to_check_index:", utterer_to_check_index)
            if utterer_to_check_index < 0:
                print("no entity found")
                self.entity = None
                break
            self.entity = utterers[utterers_keys[utterer_to_check_index]]

            # if entity not in model, keep going
            if self.entity is None:
                continue
            # if entity is a match then stop decrementing index
            #if self.entity.is_addressed == self.is_addressed:
            #    break
            match_on_all_attribs = True
            for attrib in attribs_to_check:
                if getattr(self.entity, attrib) != getattr(self, attrib):
                    match_on_all_attribs = False
                    break
            if match_on_all_attribs:
                break


    def hon_mention(self, context):
        utterers = context["utterers"]
        utterance_id = context["utterance_id"]
        model = context["model"]
        # this mention refers to someone other than the addressee
        self.is_addressed = False
        self.find_nearest_previous_utterer_matching_attributes(utterers, utterance_id, model, attribs_to_check=["is_addressed"])

    # first person pronouns
    def pronominal_mention_1(self, context):
        utterers = context["utterers"]
        utterance_id = context["utterance_id"]
        self.entity = utterers[utterance_id]

    def pronominal_mention_2(self, context):
        pass

    # todo: could use own attributes e.g. gender
    def mention_attributes_match(self, candidate_antecedent, disallowed_roles=[]):
        print("candidate antecedent:", candidate_antecedent)
        if candidate_antecedent.role not in disallowed_roles:
            return True

        return False


    # resolve third person pronouns
    def pronominal_mention_3(self, context):
        annotated_mentions = context["annotated_mentions"]
        mention_index = context["mention_index"]
        ordered_mentions = context["ordered_mentions"]
        utterance_id = context["utterance_id"]

        print("annotated mentions", annotated_mentions)
        print("mention index", mention_index)
        print("ordered_mentions in annot", ordered_mentions)
        print("for ", self)

        break_i = False
        # iterate over sentences in reverse
        for i in range(self.sentence_number, -1, -1):
            # iterate mentions left to right as in Raghunathan et al. (2010)
            for j in range(len(ordered_mentions[i])):
                # if the candidate antecedent matches then the entity can be set to match that of the antecedent and the loop can break
                if self.mention_attributes_match(annotated_mentions[ordered_mentions[i][j]], disallowed_roles=["pronominal_mention"]):
                    self.entity = annotated_mentions[ordered_mentions[i][j]].entity
                    break_i = True
                    break
            if break_i:
                break


    def pronominal_mention_other(self, context):
        pass

    def pronominal_mention(self, context):
        # now call a specific method based on the person of the pronoun
        getattr(self, f"{self.role}_{self.person}")(context)


    # assign an associated entity
    # todo: replace **context with named args, pack it into a dict and pass this into method based on string,
    #   if some context is missing, put out a warning but continue with the rest of the resolution
    def resolve(self, **context):
        #print("utterers, key", context["utterers"], context["utterance_id"], context["annotated_mentions"], context["mention_index"], context["ordered_mentions"])
        # if the entity was already set due to 1 to 1 mapping, there is no work to be done
        if self.entity is not None:
            return

        # call correct method based on role of mention
        # using getattr() is safer than using exec()
        getattr(self, self.role)(context)

    def __str__(self):
        return f"{self.start_char}, {self.end_char}\n" \
               f"{self.sentence_number}, {self.start_char_in_sentence}, {self.end_char_in_sentence}\n" \
               f"{self.person}, {self.gender}\n" \
               f"{self.rank}, shadow? {self.is_shadow}\n" \
               f"{self.role}\n" \
               f"constituency of associated MP: {self.get_associated_constituency()}"
