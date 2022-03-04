#!/bin/bash

# Use datacompy to compare all of the files in the metadata json and produce diff csv.

if [ -z $1 ] || [ -z $2 ] || [ -z $3 ] || [ -z $4 ] || [ -z $5 ]
then
  echo "Missing required arguments. Usage ./compare_files script_dir one_dir two_dir metadata.json output_dir"
fi

jq -r '.[] | [.table_name, (.join_columns | join (","))] | @tsv' $4 \
| while IFS=$'\t' read -r table_name join_tables; do
  python3 $1/compare_files.py "$2/$table_name.csv" "$3/$table_name.csv" $join_tables > "$5/$table_name-diff.csv"
  echo "Completed comparing $table_name. Wrote $5/$table_name-diff.csv"
done
