import pandas as pd

# Reads in the data
df_attr = pd.read_csv('home-depot-data/attributes.csv', encoding="ISO-8859-1")
df_attr = df_attr[df_attr.name == "MFG Brand Name"]

searchQueries = df_attr["value"].unique()
df = pd.DataFrame(searchQueries)
df.to_csv('brandnames.csv', index=False, header=False)
