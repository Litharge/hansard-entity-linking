from structure.range_level import transform_hon, WholeXMLAnnotation
import unittest
import datetime
import pickle



test_obj = WholeXMLAnnotation("test_xml/test_debate.xml",
                              "uk.org.publicwhip/debate/2020-06-15a.503.6",
                              "uk.org.publicwhip/debate/2020-06-15a.506.5",
                              "system_data/test_system_input/2021-12-01.p",
                              datetime.datetime(2021, 12, 1))

test_obj.set_references()
print("test obj")
print(test_obj)

pickle.dump(test_obj, open("system_data/system_output/test.p", "wb"))


