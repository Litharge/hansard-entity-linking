# test that creates a very limited discourse model using a small version of an MP list file

from discourse_model.get_list import save_csv
from discourse_model.create_db import create_db_from_list

test_date = "test"

create_db_from_list("test", "", test_date)




