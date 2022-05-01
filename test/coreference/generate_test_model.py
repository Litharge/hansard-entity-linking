import sys

# todo: use sys.argv to get cmd line args

from discourse_model.get_list import save_csv
from discourse_model.model_from_list import MPList

test_date = "2021-12-01"
save_csv(test_date, "./2021_12_01_list")

to_save = MPList("./2021_12_01_list", "./", test_date, create_pickle=True)
