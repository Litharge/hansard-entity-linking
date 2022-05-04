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

    def __str__(self):
        return f"{self.start_char}, {self.end_char}\n" \
               f"{self.sentence_number}, {self.start_char_in_sentence}, {self.end_char_in_sentence}\n" \
               f"{self.person}, {self.gender}\n" \
               f"{self.rank}, shadow? {self.shadow}\n" \
               f"{self.role}\n" \
               f"constituency of associated MP: {self.get_associated_constituency()}"
