#!/bin/bash

# only score the seen mock data (for testing purposes)
pipenv run scorch ../human_annotation/2020-06-15_to_score.json ../system/2021-12-01_model_output.json ./out.txt
