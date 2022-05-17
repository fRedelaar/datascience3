import pandas as pd

df_attr = pd.read_csv('brandnames.csv', encoding="ISO-8859-1")
df_attr.columns =['brands']

df_attr['brands'] = df_attr['brands'].str.lower()

df_attr.to_csv('brandnames-lower.csv', index=False, header=False)
