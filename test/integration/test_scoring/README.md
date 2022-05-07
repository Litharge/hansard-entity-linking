Directory for testing entire system on a mock xml input

Process taken
1. ran produce_text_for_humans_for_testing.py, this placed a test text file in annotated_data/human/test.txt and the corresponding
mapping in annotated_data/maps/test
2. labelled the text file in annotated_data/human/test in label studio
3. saved the annotated file in json minimal format to annotated_data/test.json
4. ran produce_test_json_from_annotated_data.py, this produces a json file ready for scoring
5. ran produce_example_model_output.py to run the system on the xml file
6. ran produce_test_json_from_model_output.py to produce the json file ready for scoring

Whenever the model is updated, rerun produce_example_model_output.py then produce_test_json_from_model_output.py.

Now the two json files are ready to have scorch run on them. This can be run with
    pipenv run scorch annotated_data/to_compare/test_gold.json system_data/to_compare/test_sys.json score_results/out.txt
and the results can be viewed in the output file. 