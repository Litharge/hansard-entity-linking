from mention_detection.produce_mentions import get_sentence_bounds, transform_hon, get_first_person_pronouns
import unittest


class TestMentions(unittest.TestCase):
    def test_get_first_person_pronouns_correct_on_natural_sentence(self):
        test_utterance = "I am sure that I've not seen it. Myself, I would prefer to hear it from a friend of mine. Come with me"

        pronoun_bounds_set = set(get_first_person_pronouns(test_utterance))

        self.assertSetEqual(pronoun_bounds_set, {(0,1), (15,16), (33,39), (41,42), (84,88), (100,102)})


if __name__ == "__main__":
    unittest.main()