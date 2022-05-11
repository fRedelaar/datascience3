import numpy as np
import pandas as pd
from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split

stemmer = SnowballStemmer('english')

# Reads in the data
og_df_train = pd.read_csv('home-depot-data/train.csv', encoding="ISO-8859-1")
og_df_test = pd.read_csv('home-depot-data/test.csv', encoding="ISO-8859-1")
df_attr = pd.read_csv('home-depot-data/attributes.csv')
df_pro_desc = pd.read_csv('home-depot-data/product_descriptions.csv')

og_df_train_without_relevance = og_df_train.drop(['relevance'], axis=1).values
og_df_train_only_relevance = og_df_train.drop(["id", "product_uid", "product_title", "search_term"], axis=1).values

x_train, x_test, y_train, y_test = train_test_split(og_df_train_without_relevance, og_df_train_only_relevance,
                                                    test_size=0.20, random_state=4)

matrix_train = pd.DataFrame(data=x_train, columns=["id", "product_uid", "product_title", "search_term"])
matrix_test = pd.DataFrame(data=x_test, columns=["id", "product_uid", "product_title", "search_term"])

num_train = matrix_train.shape[0]


def str_stemmer(s):
    return " ".join([stemmer.stem(word) for word in s.lower().split()])


def str_common_word(str1, str2):
    return sum(int(str2.find(word) >= 0) for word in str1.split())


# Creating new feature based on bullet01 in attributes.csv
df_attr_bullet = df_attr[df_attr.name == "Bullet01"]
df_attr_bullet = df_attr_bullet.drop(['name'], axis=1)

# Creating new feature based on color of product and search term
df_attr_color = df_attr[df_attr.name == "Color Family"]
df_attr_color = df_attr_color.drop(['name'], axis=1)

# Creating new feature based on brand name and search term
df_attr_brand = df_attr[df_attr.name == "MFG Brand Name"]
df_attr_brand = df_attr_brand.drop(['name'], axis=1)

# Creating column that includes name and value as 1 column
df_attr["attributes_value_and_name"] = df_attr["name"] + ' ' + df_attr["value"]
df_attr.drop(['value', 'name'], axis=1)

# Merging all rows that belong to the same product_uid as one row
df_attr = df_attr.fillna('').groupby('product_uid').attributes_value_and_name.apply(
    lambda x: ','.join(set(x))).reset_index()

df_all = pd.concat((matrix_train, matrix_test), axis=0, ignore_index=True)

df_all = pd.merge(df_all, df_pro_desc, how='left', on='product_uid')
df_all = pd.merge(df_all, df_attr, how='left', on='product_uid')
df_all = pd.merge(df_all, df_attr_brand, how='left', on='product_uid')
df_all = pd.merge(df_all, df_attr_color, how='left', on='product_uid')
df_all = pd.merge(df_all, df_attr_bullet, how='left', on='product_uid')

df_all.columns = ['id', 'product_uid', 'product_title', 'search_term',
                  'product_description', 'attributes_value_and_name', 'brand', 'color', 'bullet']

# Removing the numbers in brand names
df_all['brand'] = df_all['brand'].str.replace('\d+', '')
df_all['color'] = df_all['color'].str.replace('\d+', '')
df_all['bullet'] = df_all['bullet'].str.replace('\d+', '')

# Replacing NaN values with empty cells
df_all.attributes_value_and_name = df_all.attributes_value_and_name.fillna('')
df_all.brand = df_all.brand.fillna('')
df_all.color = df_all.color.fillna('')
df_all.bullet = df_all.bullet.fillna('')

df_all['search_term'] = df_all['search_term'].map(lambda x: str_stemmer(x))
df_all['product_title'] = df_all['product_title'].map(lambda x: str_stemmer(x))
df_all['product_description'] = df_all['product_description'].map(lambda x: str_stemmer(x))
df_all['attributes_value_and_name'] = df_all['attributes_value_and_name'].map(lambda x: str_stemmer(x))
df_all['brand'] = df_all['brand'].map(lambda x: str_stemmer(x))
df_all['color'] = df_all['color'].map(lambda x: str_stemmer(x))
df_all['bullet'] = df_all['bullet'].map(lambda x: str_stemmer(x))

df_all['len_of_query'] = df_all['search_term'].map(lambda x: len(x.split())).astype(np.int64)

df_all['product_info'] = df_all['search_term'] + "\t" + df_all['product_title'] + "\t" + df_all[
    'product_description'] + "\t" + df_all['attributes_value_and_name'] + "\t" + df_all['brand'] + "\t" + df_all[
                             'color'] + "\t" + df_all['bullet']

df_all['word_in_title'] = df_all['product_info'].map(lambda x: str_common_word(x.split('\t')[0], x.split('\t')[1]))
df_all['word_in_description'] = df_all['product_info'].map(
    lambda x: str_common_word(x.split('\t')[0], x.split('\t')[2]))
df_all['word_in_attributes'] = df_all['product_info'].map(
    lambda x: str_common_word(x.split('\t')[0], x.split('\t')[3]))
df_all['word_in_brand'] = df_all['product_info'].map(
    lambda x: str_common_word(x.split('\t')[0], x.split('\t')[4]))
df_all['word_in_color'] = df_all['product_info'].map(
    lambda x: str_common_word(x.split('\t')[0], x.split('\t')[5]))
df_all['word_in_bullet'] = df_all['product_info'].map(
    lambda x: str_common_word(x.split('\t')[0], x.split('\t')[6]))

# Dropping all duplicates that were created by the new features (such as color)
df_all = df_all.drop_duplicates(subset=['id'])

df_all = df_all.drop(
    ['search_term', 'product_title', 'product_description', 'product_info', 'attributes_value_and_name', 'brand',
     'color', 'bullet'
     ], axis=1)

df_train = df_all.iloc[:num_train]
df_test = df_all.iloc[num_train:]
id_test = df_test['id']

X_train = df_train.drop(['id'], axis=1).values
X_test = df_test.drop(['id'], axis=1).values

rf = RandomForestRegressor(n_estimators=170, max_depth=9, random_state=0)
clf = BaggingRegressor(rf, n_estimators=45, max_samples=0.1, random_state=25)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

pd.DataFrame({"id": id_test, "relevance": y_pred, "actual": y_test.flatten()}).to_csv('submission.csv', index=False)

print("RMSE: ", sqrt(mean_squared_error(y_test.flatten(), y_pred)))
