for entry in *
do
  echo "$entry"".zip"
  zip -r "$entry"".zip" "$entry"/*
done
