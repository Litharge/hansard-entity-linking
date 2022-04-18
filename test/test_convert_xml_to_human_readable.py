import unittest

from convert.convert_xml_to_human_readable import get_human_readable


class TestConvert(unittest.TestCase):
    def test_correct_range_got_multiple(self):
        test_file = "../hansard_xml/train/debates2020-06-15a.xml"
        test_start = "uk.org.publicwhip/debate/2020-06-15a.503.6"
        test_end = "uk.org.publicwhip/debate/2020-06-15a.503.7"

        result_string, result_id_ranges = get_human_readable(test_file, test_start, test_end)

        expected = """Laura Farris
What steps he is taking with Cabinet colleagues to support the wedding sector during the covid-19 outbreak. 

Chris Green
What plans he has to reopen places of worship as the covid-19 restrictions are eased. 

"""

        self.assertEqual(result_string, expected)

    # test that pid's are described by the dictionary correctly
    def test_pid_mapping(self):
        test_file = "../hansard_xml/train/debates2020-06-15a.xml"
        test_start = "uk.org.publicwhip/debate/2020-06-15a.503.6"
        test_end = "uk.org.publicwhip/debate/2020-06-15a.503.7"

        result_string, result_id_ranges = get_human_readable(test_file, test_start, test_end)

        print(result_string)

        self.assertEqual(result_id_ranges.mapping[13], "a503.6/1")
        print(result_id_ranges.mapping)
        self.assertEqual(result_id_ranges.mapping[135], "a503.7/1")
        print(result_id_ranges.mapping[13])

    def test_bisection_search_works_on_utterers(self):
        test_file = "../hansard_xml/train/debates2020-06-15a.xml"
        test_start = "uk.org.publicwhip/debate/2020-06-15a.503.6"
        test_end = "uk.org.publicwhip/debate/2020-06-15a.503.7"

        result_string, result_id_ranges = get_human_readable(test_file, test_start, test_end)

        # check that all values 0 to 12 inclusive resolve to correct utterer
        for i in range(0, 13):
            self.assertTrue(result_id_ranges.get_id(i) == "utterer_Laura Farris")

        # check that all values 123 to 134 inclusive resolve to correct utterer
        for i in range(123, 135):
            self.assertTrue(result_id_ranges.get_id(i) == "utterer_Chris Green")

if __name__ == "__main__":
    unittest.main()