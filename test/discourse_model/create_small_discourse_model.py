# test that creates a very limited discourse model using a small version of an MP list file
import unittest
import sqlite3

from discourse_model.get_list import save_csv
from discourse_model.create_db import create_db_from_list


class TestDiscourseModel(unittest.TestCase):
    def test_database_contents_mp_table(self):
        test_date = "test"

        create_db_from_list("test", "", test_date)

        conn = sqlite3.connect("test.db",
                               detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

        cursor = conn.cursor()

        with conn:
            mp_content = list(cursor.execute("SELECT * FROM mps"))

            self.assertTupleEqual(mp_content[0], ('Torbay', 'Conservative', 'Kevin', 'Foster'))
            self.assertTupleEqual(mp_content[1], ('Redditch', 'Conservative', 'Rachel', 'Maclean'))
            self.assertTupleEqual(mp_content[2], ('Hackney North and Stoke Newington', 'Labour', 'Diane', 'Abbott'))



if __name__ == "__main__":
    unittest.main()

