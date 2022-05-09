# uses convert_ to produce a text file in a specified location, along with mapping pickle
import pickle

from convert.produce_text_for_humans import save_human_readable_and_mapping
import evaluation.scripts.evaluation_files_metadata as metadata

xml_location = "test_xml/test_debate.xml"
start_utterance_id = "uk.org.publicwhip/debate/2020-06-15a.503.1"
end_utterance_id = "uk.org.publicwhip/debate/2020-06-15a.506.5"
to_annotate_save_location = "annotated_data/to_annotate/test.txt"
mapping_save_location = "annotated_data/to_annotate_maps/test"

for i in range(len(metadata.xml_locations)):
    save_human_readable_and_mapping(metadata.xml_locations[i],
                                    metadata.start_values[i],
                                    metadata.end_values[i],
                                    metadata.to_annotate_save_locations[i],
                                    metadata.mapping_save_locations[i])