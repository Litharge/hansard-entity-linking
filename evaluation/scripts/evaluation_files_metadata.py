import datetime

# model data
mock_model_date = "2020-06-15"
period_2016_model_date = "2016-03-11"
period_2020_model_date = "2020-12-14"

# shared data
mock_xml_locations = ["../xml/debates2020-06-15a.xml"]

xml_locations = [
                 "../xml/debates2016-03-11b.xml",

                 "../xml/debates2016-05-10a.xml",

                 "../xml/debates2016-05-12a.xml",
                 "../xml/debates2020-12-14b.xml",

                 "../xml/debates2020-12-16b.xml",

                 "../xml/debates2021-03-12a.xml", ]
# start positions chosen by random number generator
mock_start_values = ["uk.org.publicwhip/debate/2020-06-15a.507.7"]
start_values = [
                "uk.org.publicwhip/debate/2016-03-11b.548.9",

                "uk.org.publicwhip/debate/2016-05-10a.603.1",

                "uk.org.publicwhip/debate/2016-05-12a.710.2",
                "uk.org.publicwhip/debate/2020-12-14b.36.7",

                "uk.org.publicwhip/debate/2020-12-16b.304.0",

                "uk.org.publicwhip/debate/2021-03-12a.1200.1"

                ]


# end values are 5 utterances from the start values
mock_end_values = ["uk.org.publicwhip/debate/2020-06-15a.509.1"]
end_values = [
              "uk.org.publicwhip/debate/2016-03-11b.549.2",

              "uk.org.publicwhip/debate/2016-05-10a.604.3",

              "uk.org.publicwhip/debate/2016-05-12a.710.6",
              "uk.org.publicwhip/debate/2020-12-14b.37.3",

              "uk.org.publicwhip/debate/2020-12-16b.304.4",

              "uk.org.publicwhip/debate/2021-03-12a.1201.0"
              ]

# shared gold and manual metadata
mock_mapping_save_locations = ["../mock/2020-06-15_mapping.p"]
mapping_save_locations = [
                              "../text_for_humans/2016-03-11_mapping.p",

                              "../text_for_humans/2016-05-10_mapping.p",

                              "../text_for_humans/2016-05-12_mapping.p",
                              "../text_for_humans/2020-12-14_mapping.p",

                              "../text_for_humans/2020-12-16_mapping.p",

                              "../text_for_humans/2021-03-12_mapping.p",
                          ]


mock_to_annotate_save_locations = ["../mock/2020-06-15_to_annotate.txt"]
to_annotate_save_locations = [
                              "../text_for_humans/2016-03-11_to_annotate.txt",

                              "../text_for_humans/2016-05-10_to_annotate.txt",

                              "../text_for_humans/2016-05-12_to_annotate.txt",
                              "../text_for_humans/2020-12-14_to_annotate.txt",

                              "../text_for_humans/2020-12-16_to_annotate.txt",

                              "../text_for_humans/2021-03-12_to_annotate.txt",
                              ]

# gold only
# note that you must specify the locations you save the annotated data to from label studio in this list:
gold_annotated_save_locations = [
                            "../gold/2016-03-11_annotated.json",

                            "../gold/2016-05-10_annotated.json",

                            "../gold/2016-05-12_annotated.json",
                            "../gold/2020-12-14_annotated.json",

                            "../gold/2020-12-16_annotated.json",

                            "../gold/2021-03-12_annotated.json"
                            ]
gold_to_score_save_locations = [
                            "../gold/2016-03-11_to_score.json",

                            "../gold/2016-05-10_to_score.json",

                            "../gold/2016-05-12_to_score.json",
                            "../gold/2020-12-14_to_score.json",

                            "../gold/2020-12-16_to_score.json",

                            "../gold/2021-03-12_to_score.json"
                           ]

# manual metadata
# note that you must specify the locations you save the annotated data to from label studio in this list:
manual_annotated_save_locations = [
                            "../manual/2016-03-11_annotated.json",

                            "../manual/2016-05-10_annotated.json",

                            "../manual/2016-05-12_annotated.json",
                            "../manual/2020-12-14_annotated.json",

                            "../manual/2020-12-16_annotated.json",

                            "../manual/2021-03-12_annotated.json"
                            ]


manual_to_score_save_locations = [
                            "../manual/2016-03-11_to_score.json",

                            "../manual/2016-05-10_to_score.json",

                            "../manual/2016-05-12_to_score.json",
                            "../manual/2020-12-14_to_score.json",

                            "../manual/2020-12-16_to_score.json",

                            "../manual/2021-03-12_to_score.json"
                           ]

mock_annotated_save_locations = ["../mock/2020-06-15_annotated.json"]
mock_to_score_save_locations = ["../mock/2020-06-15_to_score.json"]

# system output only data
# datetimes used to automatically name system output
mock_dates = [datetime.datetime(2020, 6, 15)]
dates = [
         datetime.datetime(2016, 3, 11),

         datetime.datetime(2016, 5, 10),

         datetime.datetime(2016, 5, 12),
         datetime.datetime(2020, 12, 14),

         datetime.datetime(2020, 12, 16),

         datetime.datetime(2021, 3, 12)]
# there are only 3 varieties of model, as these are expensive to create and applicable to any nearby debates
mock_model_locations = ["../mock/2020-06-15.p"]
model_locations = [
                   "../system/2016-03-11.p",

                   "../system/2016-03-11.p",

                   "../system/2016-03-11.p",
                   "../system/2020-12-14.p",

                   "../system/2020-12-14.p",

                   "../system/2020-12-14.p"]

# system output info
system_output_pickle_locations = [f"../system/{date.strftime('%Y-%m-%d')}_system_output.p" for date in dates]
system_json_locations = [f"../system/{date.strftime('%Y-%m-%d')}_system_output.json" for date in dates]

# list holding location of recall, precision, f1 scores
system_entity_performance_locations = [f"../entity_performance/{date.strftime('%Y-%m-%d')}_system_entity_result.txt" for date in dates]
manual_entity_performance_locations = [f"../entity_performance/{date.strftime('%Y-%m-%d')}_manual_entity_result.txt" for date in dates]