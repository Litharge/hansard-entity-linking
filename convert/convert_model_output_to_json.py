# module to go from system output to json cluster for scorer
# result should look like: {"type": "clusters", "clusters": {"0": ["0.0-1"], "1": ["0.3-6", "1.0-0"], "2": ["1.2-3", "1.5-5", "1.7-9"]}}

import json
from pprint import pprint

from structure.range_level import WholeXMLAnnotation

def convert_model_output_to_clusters(system_output: WholeXMLAnnotation):
    #print(system_output)
    cluster_dict = {}

    for utterance_id in system_output.utterance_mentions:
        #print(utterance_id)
        for mention in system_output.utterance_mentions[utterance_id].annotated_mentions:
            if mention.entity is not None:
                #print(mention.entity.url)
                #print(mention.start_char)
                positional_identifier = f"{utterance_id}:{mention.start_char}-{mention.end_char}"
                cluster_dict.setdefault(mention.entity.url, []).append(positional_identifier)

    return {"type": "clusters", "clusters": cluster_dict}

def save_model_output_as_clusters(system_output: WholeXMLAnnotation, json_save_location):
    cluster_dict = convert_model_output_to_clusters(system_output)

    with open(json_save_location, "w") as text_file:
        text_file.write(json.dumps(cluster_dict))

    pprint(cluster_dict)

