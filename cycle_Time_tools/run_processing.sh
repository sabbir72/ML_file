#!/bin/bash

# Prompt for each input individually
echo "Please enter the following values one by one:"
# Run the Python script with collected parameters
python3 crop_txt_cycle.py "$VIDEO_DIRECTORY" "$LABEL" "$OUTPUT_BASE_DIRECTORY" "$FPS" "$NUM_CROPS"

