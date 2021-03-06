from structure.range_level import transform_hon, WholeXMLAnnotation
from convert.convert_model_output_to_json import save_model_output_as_clusters
import evaluation.scripts.evaluation_files_metadata as metadata

import unittest
import datetime
import pickle



for i in range(len(metadata.xml_locations)):
    test_obj = WholeXMLAnnotation(metadata.xml_locations[i],
                              metadata.start_values[i],
                              metadata.end_values[i],
                              metadata.model_locations[i],
                              metadata.dates[i])

    test_obj.set_references()
    print("test obj")
    print(test_obj)

    pickle.dump(test_obj, open(metadata.system_output_pickle_locations[i], "wb"))

for i in range(len(metadata.xml_locations)):
    test_system_output = pickle.load(open(metadata.system_output_pickle_locations[i], "rb"))
    save_model_output_as_clusters(test_system_output, metadata.system_json_locations[i])


