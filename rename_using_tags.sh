file=${1:?}
if exiftool ${file} | grep -q 'Title'; then
  title=$(exiftool -Title -m -p '${Title}' ${file})
else
  echo "Title tag does not exist for ${file}."
fi

if exiftool ${file} | grep -q 'Artist'; then
  artist=$(exiftool -Title -m -p '${Artist}' ${file})
else
  echo "Title tag does not exist for ${file}."
fi

echo "${title} - ${artist}"

