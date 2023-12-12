inpath=$1

for folder in $(ls $inpath); do
  echo "Computing luminosity for dataset $folder"
  for jsonfile in $(ls $inpath/$folder); do
    if [[ $jsonfile == *"json"* ]]; then
      outname=$(echo $jsonfile |  sed 's/.json//g')
      brilcalc lumi -i $inpath/$folder/$jsonfile > $inpath/$folder/$outname".txt"
    fi
  done
done

