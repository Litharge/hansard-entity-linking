from structure.range_level import transform_hon, WholeXMLAnnotation
from convert.convert_model_output_to_json import save_model_output_as_clusters

import unittest
import datetime
import pickle

xml_locations = ["../xml/debates2020-06-15a.xml"]
dates = [datetime.datetime(2021, 12, 1)]
start_values = ["uk.org.publicwhip/debate/2020-06-15a.507.7"]
end_values = ["uk.org.publicwhip/debate/2020-06-15a.509.1"]

model_locations = ["../system/2020-06-15.p"]

for i in range(len(start_values)):
    test_obj = WholeXMLAnnotation(xml_locations[i],
                                  start_values[i],
                                  end_values[i],
                                  model_locations[i],
                                  dates[i])

    test_obj.set_references()
    print("test obj")
    print(test_obj)

    pickle.dump(test_obj, open(f"../system/{dates[i].strftime('%Y-%m-%d')}_model_output.p", "wb"))

for i in range(len(dates)):
    test_system_output = pickle.load(open(f"../system/{dates[i].strftime('%Y-%m-%d')}_model_output.p", "rb"))
    save_model_output_as_clusters(test_system_output, f"../system/{dates[i].strftime('%Y-%m-%d')}_model_output.json")


