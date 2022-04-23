# user script to download populate an sqlite DB with MP information for a given session

import sys

# todo: use sys.argv to get cmd line args

from discourse_model.get_list import save_csv
from discourse_model.create_db import create_db_from_list

test_date = "2017-06-09"
save_csv("a", "../discourse_model_data/test")

create_db_from_list("../discourse_model_data/test", "../discourse_model_data/", test_date)

