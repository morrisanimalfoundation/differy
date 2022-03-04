import sys
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Set the default seaborn theme, overriding matplotlib.
sns.set_theme()

# Read the diff file into a dataframe.
df1 = pd.read_csv(sys.argv[1], low_memory=False)

if not {'relationship_category'}.issubset(df1.columns):
    df1['relationship_category'] = 'DOG'

# Extract only the match columns and join tables.
# Then group the dataframe by relationship_category
# Todo use join_tables in sys.argv[2].
to_date = int(sys.argv[3])
relationship_groups = df1[df1["to_date"] == to_date].filter(regex='study_year|relationship_category|_match$').groupby(
    ['relationship_category'])

# Get the  human name for the subject.
subject_title = sys.argv[4]

# Tell matplotlib we expect a 2x2 grid of plots, set size expectations, name etc.
row_column_count = 2 if relationship_groups.ngroups > 2 else 1
# Todo only create as many plots as we have relationship categories.
fig, ax = plt.subplots(row_column_count, row_column_count, sharex=True, figsize=(12, 9), layout='constrained')
fig.suptitle('Conditions ' + subject_title)

# When dealing with subplots matplotlib references them as a grid.
# Store the grid coordinates as a tuple for easy mapping to single loop.
ax_count = 0
ax_keys = ((0, 0), (0, 1), (1, 0), (1, 1))

# Start massaging our data.
# At this point all records are grouped by relationship value.
for relationship_group_key, relationship_group_value in relationship_groups:
    # Build a new dataframe that will store aggregated values, counts of _match columns.
    aggregate_df = pd.DataFrame({'year': [], 'condition': [], 'change': []})
    # Group our already grouped data by year, because we want to see _match counts by year.
    year_groups = relationship_group_value.groupby(['study_year'])
    for year_group_key, year_group_value in year_groups:
        # Get only the _match columns as a dataframe.
        boolean_columns_df = year_group_value.filter(regex='_match$')
        # Create a series where all _match_columns with False values are summed.
        boolean_columns_series = boolean_columns_df[boolean_columns_df == False].count(axis=0)
        # Build our final dataframe.
        for index, value in boolean_columns_series.items():
            aggregate_df.loc[len(aggregate_df.index)] = {'year': year_group_key, 'condition': index, 'change': value}
    # Arrange the data so that the axes are as we'd like and remove the _match park of the column name.
    final_df = aggregate_df.pivot('condition', 'year', 'change').rename(lambda column: column.replace('_match', ''))
    if row_column_count == 1:
        ax.set_title(relationship_group_key)
        sns.heatmap(final_df, linewidths=.5, ax=ax)
    else:
        # Name our quadrant.
        ax.item(ax_keys[ax_count]).set_title(relationship_group_key)
        # Build a chart.
        sns.heatmap(final_df, linewidths=.5, ax=ax.item(ax_keys[ax_count]))
    ax_count += 1

if row_column_count == 2:
    i = relationship_groups.ngroups
    while i <= 3:
        ax.item(ax_keys[i]).remove()
        i += 1

# Output the png to the output dir.
plt.savefig(sys.argv[5] + '/' + subject_title.lower().replace(' ', '_') + '.png')
