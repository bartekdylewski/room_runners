#!/bin/bash

input_dir="./input"
inputlong_dir="./inputlong"
inputend_dir="./inputend"

# create folders if not existing
mkdir -p "$input_dir" "$inputlong_dir" "$inputend_dir"

# generate and test
# off to see the wizard
while true; do
  python3 generator.py
  python3 rooms.py
done