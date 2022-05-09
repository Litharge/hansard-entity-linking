#!/bin/bash

# only score the seen mock data (for testing purposes)
pipenv run scorch ../mock/2020-06-15_to_score.json ../mock/2020-06-15_system_output.json ../mock/out.txt
