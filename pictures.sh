#!/bin/bash

# Transform diff data via pandas dataframe manipulation and use seaborn/matplotlib to create visualization pngs.

if [ -z $1 ] || [ -z $2 ] || [ -z $3 ] || [ -z $4 ]
then
  echo "Missing required arguments. Usage ./pictures script_dir input_dir metadata.json output_dir"
fi

jq -r '.[] | [.label, .table_name, (.join_columns | join (","))] | @tsv' $3 \
| while IFS=$'\t' read -r label table_name join_columns; do
  #python3 $1/pictures.py "$2/$table_name-diff.csv" $join_columns "1" "$label to date" $4
  python3 $1/pictures.py "$2/$table_name-diff.csv" $join_columns "0" "$label" $4
  echo "Created visualization for $table_name in $4"
done
