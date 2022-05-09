from convert.convert_annotated_data_to_json import produce_clusters
import evaluation.scripts.evaluation_files_metadata as metadata

for i in range(len(metadata.mock_annotated_save_locations)):
    produce_clusters(metadata.mock_annotated_save_locations[i],
                     metadata.mock_mapping_save_locations[i],
                     metadata.mock_to_score_save_locations[i])
