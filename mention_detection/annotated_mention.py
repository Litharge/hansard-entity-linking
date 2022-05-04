# todo: place call to get_matching_antecedent() in here, this will be a function in a coreference subpackage that
#  takes in params for what type of mention to look for then return the matching chain id
#  MAYBE place AnnotatedMention in the coreference package, then Mentions is seen as detecting the mentions, ready
#  for them to perform coref resolution
# instances represent mentions in sentences
# can take on additional data e.g. linking to a cluster
class AnnotatedMention():
    def __init__(self, start_char=None, end_char=None, sentence=None, start_char_in_sentence=None,
                                      end_char_in_sentence=None, person=None, gender=None, rank=None, shadow=None, role=None, entity=None):
        # syntactic info
        self.start_char = start_char
        self.end_char = end_char

        self.sentence_number = sentence
        self.start_char_in_sentence = start_char_in_sentence
        self.end_char_in_sentence = end_char_in_sentence

        self.person = person
        self.gender = gender

        self.rank = rank
        self.shadow = shadow

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

    def member_for_mention(self, utterers, utterance_id):
        print("in member_for_mention")
    def irregular_office_mention(self, utterers, utterance_id):
        pass
    def speaker_mention(self, utterers, utterance_id):
        pass
    def exact_nominal_mention(self, utterers, utterance_id):
        pass
    def exact_office_mention(self, utterers, utterance_id):
        pass
    def secretary_regular_mention(self, utterers, utterance_id):
        pass
    def minister_class_mention(self, utterers, utterance_id):
        pass
    def deputy_speaker_mention(self, utterers, utterance_id):
        pass
    def hon_mention(self, utterers, utterance_id):
        pass

    # first person pronouns
    def pronominal_mention_1(self, utterers, utterance_id):
        self.entity = utterers[utterance_id]
    def pronominal_mention_2(self, utterers, utterance_id):
        pass
    def pronominal_mention_3(self, utterers, utterance_id):
        pass
    def pronominal_mention_other(self, utterers, utterance_id):
        pass

    def pronominal_mention(self, utterers, utterance_id):
        # now call a specific method based on the person of the pronoun
        getattr(self, f"{self.role}_{self.person}")(utterers, utterance_id)


    # assign an associated entity
    def resolve(self, utterers, utterance_id):
        print("utterers, key", utterers, utterance_id)
        # if the entity was already set due to 1 to 1 mapping, there is no work to be done
        if self.entity is not None:
            return

        # call correct method based on role of mention
        # using getattr() is safer than using exec()
        getattr(self, self.role)(utterers, utterance_id)

    def __str__(self):
        return f"{self.start_char}, {self.end_char}\n" \
               f"{self.sentence_number}, {self.start_char_in_sentence}, {self.end_char_in_sentence}\n" \
               f"{self.person}, {self.gender}\n" \
               f"{self.rank}, shadow? {self.shadow}\n" \
               f"{self.role}\n" \
               f"constituency of associated MP: {self.get_associated_constituency()}"
