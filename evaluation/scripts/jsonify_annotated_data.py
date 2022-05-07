from convert.convert_annotated_data_to_json import produce_clusters

annotated_save_locations = ["../human_annotation/2020-06-15_annotated.json"]
mapping_save_locations = ["../human_annotation/2020-06-15_mapping.p"]
to_score_save_locations = ["../human_annotation/2020-06-15_to_score.json"]

for i in range(len(annotated_save_locations)):
    produce_clusters(annotated_save_locations[i], mapping_save_locations[i], to_score_save_locations[i])
