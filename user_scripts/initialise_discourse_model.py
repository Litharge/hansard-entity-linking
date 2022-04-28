# user script to download populate an sqlite DB with MP information for a given session

import sys

# todo: use sys.argv to get cmd line args

from discourse_model.get_list import save_csv
from discourse_model.create_db import MPList

test_date = "2020-06-15"
save_csv(test_date, "../discourse_model_data/test")

to_save = MPList("../discourse_model_data/test", "../discourse_model_data/", test_date, create_pickle=True)

