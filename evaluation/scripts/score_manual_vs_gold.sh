#!/bin/bash

# score the manual annotation using the gold data
pipenv run scorch ../gold/2016-03-11_to_score.json ../manual/2016-03-11_to_score.json ../performance/2016-03-11_manual_result.txt
pipenv run scorch ../gold/2016-05-10_to_score.json ../manual/2016-05-10_to_score.json ../performance/2016-05-10_manual_result.txt
pipenv run scorch ../gold/2016-05-12_to_score.json ../manual/2016-05-12_to_score.json ../performance/2016-05-12_manual_result.txt
pipenv run scorch ../gold/2020-12-14_to_score.json ../manual/2020-12-14_to_score.json ../performance/2020-12-14_manual_result.txt
pipenv run scorch ../gold/2020-12-16_to_score.json ../manual/2020-12-16_to_score.json ../performance/2020-12-16_manual_result.txt
pipenv run scorch ../gold/2021-03-12_to_score.json ../manual/2021-03-12_to_score.json ../performance/2021-03-12_manual_result.txt
