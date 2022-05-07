# user script to download populate an sqlite DB with MP information for a given session

import sys

# todo: use sys.argv to get cmd line args

from discourse_model.get_list import save_csv
from discourse_model.model_from_list import MPList

test_date = "2020-06-15"
test_list_location = "./test_mp_list"
save_csv(test_date, test_list_location)

to_save = MPList(test_list_location, "./", test_date, create_pickle=True)

