#!/bin/bash

input_dir="./input"
inputlong_dir="./inputlong"
inputend_dir="./inputend"

# create folders if not existing
mkdir -p "$input_dir" "$inputlong_dir" "$inputend_dir"

# generate and test
# off to see the wizard
while true; do
  # run generator
  python "./generator.py"
  
  # check if generated.txt exists
  if [[ -f "$input_dir/generated.txt" ]]; then
    # run rooms.py and measure time
    start=$(date +%s%N)
    python "./rooms.py"
    end=$(date +%s%N)

    # time in ms
    duration=$(( (end - start) / 1000000 ))

    echo "Execution time: ${duration}ms"
  else
    echo "Error: generated.txt not found"
  fi
done
