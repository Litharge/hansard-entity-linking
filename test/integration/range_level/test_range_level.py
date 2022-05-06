from structure.range_level import transform_hon, WholeXMLAnnotation
import unittest
import datetime


class TestMentions(unittest.TestCase):
    def test_hon_transform(self):
        test_utterance_span_original = "The hon. Gentleman is at least partly correct. There will be additional costs to " \
                              "maintaining the Vanguard class through to 2028."

        test_utterance_span = transform_hon(test_utterance_span_original)

        test_utterance_span_expected = "The hon  Gentleman is at least partly correct. There will be additional costs to " \
                                       "maintaining the Vanguard class through to 2028."

        self.assertEqual(test_utterance_span, test_utterance_span_expected)

    def test_output(self):
        test_obj = WholeXMLAnnotation("test_debate.xml",
                                      "uk.org.publicwhip/debate/2020-06-15a.503.6",
                                      "uk.org.publicwhip/debate/2020-06-15a.506.5",
                                      "2021-12-01.p",
                                      datetime.datetime(2021, 12, 1))

        print(test_obj)

    def test_output_full(self):
        test_obj = WholeXMLAnnotation("test_debate.xml",
                                      "uk.org.publicwhip/debate/2020-06-15a.503.6",
                                      "uk.org.publicwhip/debate/2020-06-15a.506.5",
                                      "2021-12-01.p",
                                      datetime.datetime(2021, 12, 1))

        test_obj.set_references()
        print("test obj")
        print(test_obj)

if __name__ == "__main__":
    unittest.main()

