# module containing function allowing the saving of a human readable and annotatable version of some xml
import pickle

from convert.convert_xml_to_human_readable import get_human_readable

def save_human_readable_and_mapping(xml_location, start_utterance_id, end_utterance_id, to_annotate_save_location, mapping_save_location):
    result = get_human_readable(xml_location, start_utterance_id, end_utterance_id)

    print(result[0])
    print(result[1].mapping)

    with open(to_annotate_save_location, "w") as text_file:
        text_file.write(result[0])

    pickle.dump(result[1].mapping, open(mapping_save_location, "wb"))
