#!/bin/bash

# Loop over all MP4 files in the current directory
for file in *.mp4; do
  # Extract the filename without the extension
  filename="${file%.*}"

  # Use ffmpeg to extract subtitles (assuming stream 0:s:0 contains subtitles)
  ffmpeg -i "$file" -map 0:s:0 "${filename}.srt"
  
  # Check if the extraction was successful
  if [ $? -eq 0 ]; then
    echo "Subtitles extracted successfully for $file"
  else
    echo "Failed to extract subtitles for $file"
  fi
done
