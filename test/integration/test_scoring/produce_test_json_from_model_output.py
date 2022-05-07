import pickle

from convert.convert_model_output_to_json import save_model_output_as_clusters

test_system_output = pickle.load(open("system_data/system_output/test.p", "rb"))
save_model_output_as_clusters(test_system_output, "system_data/to_compare/test_sys.json")