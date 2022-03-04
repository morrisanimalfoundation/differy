#!/bin/bash

# Executed inside of a mysql enabled container to dump tables listed in the json metadata file.

if [ -z $1 ] || [ -z $2 ] || [ -z $3 ]
then
  echo "Missing required arguments. Usage ./conditions_harvest sql_file.sql metadata.json output_dir"
fi

# Mysql is not always running in the containers.
service mysql start

# Make sure the database is present.
mysql -u root -proot -e 'CREATE DATABASE grls_ubc_normalized'
# Import the datas.
mysql -u root -proot grls_ubc_normalized < $1

# Loop through the metadata and dump the tables we care about to tsvs.
for table_name in $(jq -r '.[].table_name' $2); do
  mysql -u root -proot grls_ubc_normalized -e "SELECT * FROM $table_name" > "$3/$table_name.tsv"
  echo "Completed dumping table $table_name to $3/$table_name.tsv"
done