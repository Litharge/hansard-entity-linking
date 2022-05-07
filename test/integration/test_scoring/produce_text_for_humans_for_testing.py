# uses convert_ to produce a text file in a specified location, along with mapping pickle
import pickle

from convert.produce_text_for_humans import save_human_readable_and_mapping

xml_location = "test_xml/test_debate.xml"
start_utterance_id = "uk.org.publicwhip/debate/2020-06-15a.503.1"
end_utterance_id = "uk.org.publicwhip/debate/2020-06-15a.506.5"
to_annotate_save_location = "annotated_data/to_annotate/test.txt"
mapping_save_location = "annotated_data/to_annotate_maps/test"

save_human_readable_and_mapping(xml_location, start_utterance_id, end_utterance_id, to_annotate_save_location, mapping_save_location)





