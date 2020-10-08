#!/bin/bash
#set -x

export CLOUDSDK_PYTHON=$(printenv CLOUDSDK_PYTHON)

LAST_ADDED_FILE=last_added_file.txt
ALL_FILES=all_files_in_bucket.txt
BUCKET=billing-livecloud-gcp

#activate gCloud account
gcloud auth activate-service-account --key-file=gcloud-credentials.json

#creating pointer file
touch $LAST_ADDED_FILE

#echo "2020-09-09T13:01:49Z" > last_added_file.txt
MATCH=$(cat $LAST_ADDED_FILE)

#check or create list of all files in bucket
if [ -f $ALL_FILES ]; then
   echo "" > $ALL_FILES
else
  touch $ALL_FILES
fi
gsutil ls -l gs://$BUCKET/** | sort -k 2 >> $ALL_FILES

OLD_IFS=$IFS
export IFS=$'\n'

#remove all lines including matching file
REMAINING_FILES=$(awk  "f;/$MATCH/{f=1}" $ALL_FILES )

BUCKET_PATH=/tmp/$BUCKET

mkdir -p $BUCKET_PATH
rm -rf $BUCKET_PATH/*


for file in $REMAINING_FILES
do
  if [[ $file == *TOTAL* ]]; then
    break
  fi
  BUCKET_FILE=$(echo $file | awk '{print $3}')
  FILE_NAME=$(echo ${BUCKET_FILE##*/})
  FILE_NAME=$(basename "$FILE_NAME" .json)
  CSV_FILE=$BUCKET_PATH/$FILE_NAME.csv

  gsutil cp -R  $BUCKET_FILE $BUCKET_PATH
  sed -r 's%\"([0-9\.]+)\"%\1%g' $BUCKET_PATH/$FILE_NAME.json > /tmp/$FILE_NAME.json
  python -m libjson2csv.json_2_csv --m /tmp/$FILE_NAME.json $CSV_FILE
  sed -i -E '0,/([a-zA-Z]*)(\.)([a-zA-Z]*)/{s/([a-zA-Z]*)(\.)([a-zA-Z]*)/\1\_\3/g}' $CSV_FILE
  echo "Transferring..."
  elasticsearch_loader  --es-host http://elasticsearch:9200 --index gcloud_billing --type count csv $CSV_FILE
  echo $file | awk '{print $2}' | tail -1 > $LAST_ADDED_FILE
#  break
done
export IFS=$OLD_IFS

#cleanup
rm -rf $BUCKET_PATH/*
