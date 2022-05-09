from structure.range_level import transform_hon, WholeXMLAnnotation
from convert.convert_model_output_to_json import save_model_output_as_clusters
import evaluation.scripts.evaluation_files_metadata as metadata

import unittest
import datetime
import pickle



for i in range(len(metadata.mock_xml_locations)):
    test_obj = WholeXMLAnnotation(metadata.mock_xml_locations[i],
                              metadata.mock_start_values[i],
                              metadata.mock_end_values[i],
                              metadata.mock_model_locations[i],
                              metadata.mock_dates[i])

    test_obj.set_references()
    print("test obj")
    print(test_obj)

    pickle.dump(test_obj, open(f"../mock/{metadata.mock_dates[i].strftime('%Y-%m-%d')}_system_output.p", "wb"))

for i in range(len(metadata.mock_xml_locations)):
    test_system_output = pickle.load(open(f"../mock/{metadata.mock_dates[i].strftime('%Y-%m-%d')}_system_output.p", "rb"))
    save_model_output_as_clusters(test_system_output, f"../mock/{metadata.mock_dates[i].strftime('%Y-%m-%d')}_system_output.json")


