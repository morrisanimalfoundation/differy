## Differy unlike a cheesery in almost every way
A set of Docker based scripts to visualize differences in large datasets. Visualizations are png files created by [seaborn](https://seaborn.pydata.org/index.html). Eventually, the goal of this tool is to provide at a glance visual QA of the GRLS UBC dataset.

We begin with two complete databases for comparison. Tables included in data-definition.json are dumped as tsv files. These are compared via [datacompy](https://capitalone.github.io/datacompy/), which creates summary csvs. The summary csvs are then massaged and visualized.

### Usage

1. Make sure images are built for the given host (`docker images`). If not, build them via: `docker build --target=mysql-env -t=<some name> .` and `docker build --target=python-env -t=<some name> .` These containers based on these images execute all steps of the script.
2. Create a workdir directory with subdirectories: one, two, comparison and app. Define the workdir in init.sh.
3. Make bash scripts executeable and run `./init.sh`