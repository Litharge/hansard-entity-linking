import evaluation.scripts.evaluation_files_metadata as metadata
from evaluation.statistics.measures import get_recall_for_dictionary, get_precision_for_dictionary, get_f1_for_dictionary
import json

for i in range(len(metadata.gold_to_score_save_locations)):
    gold = json.load(open(metadata.gold_to_score_save_locations[i]))["clusters"]
    sys = json.load(open(metadata.system_json_locations[i]))["clusters"]
    recall = get_recall_for_dictionary(gold, sys)
    precision = get_precision_for_dictionary(gold, sys)
    f1 = get_f1_for_dictionary(gold, sys)

    with open(metadata.system_entity_performance_locations[i], "w") as text_file:
        text_file.write(f"recall:\t{recall}\nprecision:\t{precision}\nf1:\t{f1}")

for i in range(len(metadata.gold_to_score_save_locations)):
    gold = json.load(open(metadata.gold_to_score_save_locations[i]))["clusters"]
    manual = json.load(open(metadata.manual_to_score_save_locations[i]))["clusters"]
    recall = get_recall_for_dictionary(gold, manual)
    precision = get_precision_for_dictionary(gold, manual)
    f1 = get_f1_for_dictionary(gold, manual)

    with open(metadata.manual_entity_performance_locations[i], "w") as text_file:
        text_file.write(f"recall:\t{recall}\nprecision:\t{precision}\nf1:\t{f1}")






