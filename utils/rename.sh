for file in *.zip
do
 mv "$file" "${file%.zip}.cbz"
done
