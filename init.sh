#!/bin/bash
host_workdir='/Users/leokacenjar/Projects/automation-scripts/differy'
database_one="/workdir/grls_ubc_normalized-2020-11-29-03-50-40.sql"
database_two="/workdir/grls_ubc_normalized-borked.sql"
definition_file="/workdir/data_definition.json"
output_directory="/workdir/output"
gitlab_project_id="find in settings"
gitlab_token="token"
gitlab_wiki_slug="slug"

# Import the first database and export our raw tsv data for tables found in json.
# If we are dealing with a truth database that is always the same, we could consider creating an image for reuse here.
# That would speed the whole thing up substantially.
echo "[Step 1] Extracting data from sql database one: $database_one > $output_directory/one"
docker run -it --rm -v $host_workdir:/workdir differy-mysql /workdir/table_harvest.sh $database_one $definition_file "$output_directory/one"

# Import the second database and export our raw tsv data for tables found in json.
echo "[Step 2] Extracting data from sql database two: $database_two > $output_directory/two"
docker run -it --rm -v $host_workdir:/workdir differy-mysql /workdir/table_harvest.sh $database_two $definition_file "$output_directory/two"

# Use datacompy to create diff csvs for each of our datasets found in json.
echo "[Step 3] Creating diff csvs in $output_directory/comparison"
docker run -it --rm -v $host_workdir:/workdir differy-python /workdir/compare_files.sh $output_directory/one $output_directory/two $definition_file $output_directory/comparison

# Create our visualizations via seaborn output as pngs.
echo "[Step 4] Creating visualizations from diff files in $output_directory/app"
docker run -it --rm -v $host_workdir:/workdir differy-python /workdir/pictures.sh $output_directory/comparison $definition_file $output_directory/app/images

# Create our "app" html file with our visualizations and from gitlab.
echo "[Step 5] Creating app html file from diff files in $output_directory/app"
docker run -it --rm -v $host_workdir:/workdir differy-python python3 build_app.py $gitlab_token $gitlab_project_id $gitlab_wiki_slug $output_directory/app/images > $output_directory/app

echo "All done!"

