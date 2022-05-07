# module to go from label studio json-min output to json cluster for scorer
# output is a list containing a single dictionary, in that dictionary the dictionary of interest is called "label"
# "label" contains a list of dictionaries, each dictionary has "start", "end" and "labels"
# result should look like: {"type": "clusters", "clusters": {"0": ["0.0-1"], "1": ["0.3-6", "1.0-0"], "2": ["1.2-3", "1.5-5", "1.7-9"]}}

# so need to iterate over "label", creating a dictionary where

import json
import pickle

# find the character number of the utterance start and it's id for a given start
def find_utterance_start_and_id(start, mapping):
    prev_key = 0
    for key in mapping:
        if start < key and start >= prev_key:
            sent_start = prev_key
            print("for", start, sent_start, mapping[sent_start])
            return prev_key, mapping[prev_key]
        prev_key = key

    # if a matching key was not found by the above , that is because the loop can not assign to the last key, in this
    # case, return the last key
    return list(mapping.keys())[-1], mapping[list(mapping.keys())[-1]]

def produce_clusters(gold_source_location, mapping_source_location, output_location):
    mapping = pickle.load(open(mapping_source_location, "rb"))
    gold = json.load(open(gold_source_location, "r"))

    print(gold)

    labels = gold[0]["label"]

    processed = {}

    for l in labels:
        start = l["start"]
        end = l["end"]
        label = l["labels"][0]
        utterance_start, utterance_id = find_utterance_start_and_id(start, mapping)

        print("start: ", start, "in", utterance_start, "with id", utterance_id)

        start_relative_to_utterance = start - utterance_start
        end_relative_to_utterance = end - utterance_start

        processed.setdefault(label, []).append(
            f"{utterance_id}:{start_relative_to_utterance}-{end_relative_to_utterance}"
        )

    result = {"type": "clusters", "clusters": processed}

    with open(output_location, "w") as text_file:
        text_file.write(json.dumps(result))

