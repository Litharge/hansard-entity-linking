# uses convert_ to produce a text file in a specified location, along with mapping pickle
import pickle

from convert.produce_text_for_humans import save_human_readable_and_mapping

xml_location = "test_xml/test_debate.xml"
start_utterance_id = "uk.org.publicwhip/debate/2020-06-15a.503.1"
end_utterance_id = "uk.org.publicwhip/debate/2020-06-15a.506.5"
to_annotate_save_location = "annotated_data/to_annotate/test.txt"
mapping_save_location = "annotated_data/to_annotate_maps/test"

xml_locations = ["../xml/debates2020-06-15a.xml"]
start_values = ["uk.org.publicwhip/debate/2020-06-15a.507.7"]
end_values = ["uk.org.publicwhip/debate/2020-06-15a.509.1"]
to_annotate_save_locations = ["../human_annotation/2020-06-15_to_annotate.txt"]
mapping_save_locations = ["../human_annotation/2020-06-15_mapping.p"]

for i in range(len(xml_locations)):
    save_human_readable_and_mapping(xml_locations[i],
                                    start_values[i],
                                    end_values[i],
                                    to_annotate_save_locations[i],
                                    mapping_save_locations[i])





