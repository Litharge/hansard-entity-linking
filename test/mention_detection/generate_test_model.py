# user script to download populate an sqlite DB with MP information for a given session

import sys

# todo: use sys.argv to get cmd line args

from discourse_model.get_list import save_csv
from discourse_model.model_from_list import MPList

to_save = MPList("./test", "./", "verified_test_discourse_model", create_pickle=True)

