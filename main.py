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


df_all = pd.concat((matrix_train, matrix_test), axis=0, ignore_index=True)

df_all = pd.merge(df_all, df_pro_desc, how='left', on='product_uid')

df_all.columns = ['id', 'product_uid', 'product_title', 'search_term', 'product_description']

df_all['search_term'] = df_all['search_term'].map(lambda x: str_stemmer(x))
df_all['product_title'] = df_all['product_title'].map(lambda x: str_stemmer(x))
df_all['product_description'] = df_all['product_description'].map(lambda x: str_stemmer(x))

df_all['len_of_query'] = df_all['search_term'].map(lambda x: len(x.split())).astype(np.int64)

df_all['product_info'] = df_all['search_term'] + "\t" + df_all['product_title'] + "\t" + df_all['product_description']

df_all['word_in_title'] = df_all['product_info'].map(lambda x: str_common_word(x.split('\t')[0], x.split('\t')[1]))
df_all['word_in_description'] = df_all['product_info'].map(
    lambda x: str_common_word(x.split('\t')[0], x.split('\t')[2]))


df_all = df_all.drop(
    ['search_term', 'product_title', 'product_description', 'product_info'], axis=1)

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
