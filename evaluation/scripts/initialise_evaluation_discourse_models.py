# creates the initial discourse model ready for use by mock, human and system scoring

import sys

# todo: use sys.argv to get cmd line args

from discourse_model.get_list import save_csv
from discourse_model.model_from_list import MPList
import evaluation.scripts.evaluation_files_metadata as metadata

# get discourse model for use in mock (debates2020-06-15a.xml)
test_date = "2020-06-15"
mock_list_location = f"../mock/{metadata.mock_model_date}_list"
save_csv(metadata.mock_model_date, mock_list_location)

to_save = MPList(mock_list_location, "../mock/", test_date, create_pickle=True)

# get discourse model for 1998 evaluation
eval_2016_start_period_date = "2016-03-11"
eval_2016_list_location = f"../system/{metadata.period_2016_model_date}_list"
save_csv(metadata.period_2016_model_date, eval_2016_list_location)

obj_1 = MPList(eval_2016_list_location, "../system/", eval_2016_start_period_date, create_pickle=True)

# get discourse model for 2020/21 evaluation
eval_2020_start_period_date = "2020-12-14"
eval_2020_list_location = f"../system/{metadata.period_2020_model_date}_list"
save_csv(metadata.period_2020_model_date, eval_2020_list_location)

obj_2 = MPList(eval_2020_list_location, "../system/", eval_2020_start_period_date, create_pickle=True)

