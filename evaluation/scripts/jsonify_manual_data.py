from convert.convert_annotated_data_to_json import produce_clusters
import evaluation.scripts.evaluation_files_metadata as metadata

for i in range(len(metadata.manual_annotated_save_locations)):
    produce_clusters(metadata.manual_annotated_save_locations[i],
                     metadata.mapping_save_locations[i],
                     metadata.manual_to_score_save_locations[i])
