#!/bin/bash

# score the system output using the gold data
pipenv run scorch ../gold/2016-03-11_to_score.json ../system/2016-03-11_system_output.json ../performance/2016-03-11_system_result.txt
pipenv run scorch ../gold/2016-05-10_to_score.json ../system/2016-05-10_system_output.json ../performance/2016-05-10_system_result.txt
pipenv run scorch ../gold/2016-05-12_to_score.json ../system/2016-05-12_system_output.json ../performance/2016-05-12_system_result.txt
pipenv run scorch ../gold/2020-12-14_to_score.json ../system/2020-12-14_system_output.json ../performance/2020-12-14_system_result.txt
pipenv run scorch ../gold/2020-12-16_to_score.json ../system/2020-12-16_system_output.json ../performance/2020-12-16_system_result.txt
pipenv run scorch ../gold/2021-03-12_to_score.json ../system/2021-03-12_system_output.json ../performance/2021-03-12_system_result.txt
