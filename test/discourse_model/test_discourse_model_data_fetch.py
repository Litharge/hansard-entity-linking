import unittest
import datetime

from discourse_model.model_from_list import MPList

class TestObjectCreation(unittest.TestCase):
    def setUp(self):
        print("here")
        self.test_obj = MPList(list_file="test", directory="./", date="test", create_pickle=True)

    def test_first_names(self):
        first_names_only = [x.first_name for x in self.test_obj.mp_list]

        expected = ["Kevin", "Rachel", "Diane"]

        self.assertListEqual(first_names_only, expected)

    def test_last_names(self):
        last_names_only = [x.last_name for x in self.test_obj.mp_list]

        expected = ["Foster", "Maclean", "Abbott"]

        self.assertListEqual(last_names_only, expected)

    def test_current_offices(self):
        self.assertTrue(self.test_obj.mp_list[0].current_offices == {'The Parliamentary Under-Secretary of State for the Home Department': datetime.datetime(2019, 12, 16, 0, 0)} )

