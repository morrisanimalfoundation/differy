import sys
import pandas as pd
import datacompy

df1 = pd.read_csv(sys.argv[1], low_memory=False, sep=",")
df2 = pd.read_csv(sys.argv[2], low_memory=False, sep=",")

join_columns = sys.argv[3].split(',')
# Create an outer join of our two datasets.
# datacompy doesn't inherently support left only or right only data, so we need to pad accordingly.
outer_join = df1.merge(
    df2, how="outer", suffixes=("_df1", "_df2"), indicator=True, **{"on": join_columns}
)
# Pad the left dataset.
right_columns = df2.columns.map(lambda column: column if column in join_columns else column + '_df1')
df1 = df1.append(outer_join[outer_join["_merge"] == "right_only"][right_columns].rename(
    lambda column: column if column in join_columns else column.replace('_df1', ''), axis=1)
)
# Pad the right dataset.
left_columns = df2.columns.map(lambda column: column if column in join_columns else column + '_df2')
df2 = df2.append(outer_join[outer_join["_merge"] == "left_only"][left_columns].rename(
    lambda column: column if column in join_columns else column.replace('_df2', ''), axis=1)
)

# Perform the compare.
compare = datacompy.Compare(
    df1,
    df2,
    join_columns=join_columns,
    abs_tol=0,
    rel_tol=0,
    df1_name=sys.argv[1],
    df2_name=sys.argv[2])
# In case we have disparate columns make sure we include them.
compare.matches(ignore_extra_columns=False)

# Output for someone to collect.
print(compare.intersect_rows.to_csv())
