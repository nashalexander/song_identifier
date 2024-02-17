#!/bin/bash

MV_CMD=mv

# Dry run
if [[ "$1" = "-d" ]]; then
  MV_CMD=echo
  shift
fi

all_files="$@"

for file in ${all_files}; do
  title=""
  artist=""

  if exiftool ${file} | grep -q 'Title'; then
    title=$(exiftool -Title -m -p '${Title}' ${file})
  else
    continue
  fi

  if exiftool ${file} | grep -q 'Artist'; then
    artist=$(exiftool -Title -m -p '${Artist}' ${file})
  fi

  file_ext="${file##*.}"

  echo "${file} : ${title} - ${artist}.${file_ext}"
  echo "rename file? (y/N)"
  
  read answer
  if [[ "${answer}" = "y" ]] || [[ "${answer}" = "Y" ]]; then
      file_ext="${file##*.}"
      
      $MV_CMD "${file}" "${title} - ${artist}.${file_ext}"
  else
      echo "${file} not renamed"
  fi

done