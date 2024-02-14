---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.1
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python pycharm={"is_executing": true}
import pandas as pd
from copy import copy
from sklearn.cluster import DBSCAN, OPTICS, KMeans
from sklearn import metrics
from sklearn.manifold import TSNE
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.model_selection import ParameterGrid
```

Общие функции

```python pycharm={"is_executing": true}
def plots(X, y, y_num):
    X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3)
    qw = X_embedded.fit_transform(X)
    n_df = pd.DataFrame(qw, columns=['x', 'y'])
    y = y.fillna(0)
    n_df['cluster_number'] = y_num
    n_df['cluster_name'] = y

    marked_df = n_df[n_df.cluster_name != 0]
    unmarked_df = n_df[n_df.cluster_name == 0]

    fig = px.scatter(n_df, x="x", y="y", color="cluster_number")
    fig1 = px.scatter(marked_df, x="x", y="y", color="cluster_name")

    fig1.add_trace(
        go.Scatter(
            mode='markers',
            x=unmarked_df.x,
            y=unmarked_df.y,
            opacity=0.3,
            marker=dict(
                color='gray',
                )
            )
    )


    fig.show()
    fig1.show()
```

```python
def plots_to_pres(X, y, y_num, y_num_map):
    X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3)
    qw = X_embedded.fit_transform(X)
    n_df = pd.DataFrame(qw, columns=['x', 'y'])
    y = y.fillna(0)
    n_df['cluster_number'] = y_num
    n_df['cluster_name'] = y
    n_df['cluster_name_map'] = y_num_map

    marked_df = n_df[n_df.cluster_name != 0]
    unmarked_df = n_df[n_df.cluster_name == 0]

    fig = px.scatter(n_df, x="x", y="y", color="cluster_number")
    fig1 = px.scatter(marked_df, x="x", y="y", color="cluster_name")

    fig1.add_trace(
        go.Scatter(
            mode='markers',
            x=unmarked_df.x,
            y=unmarked_df.y,
            opacity=0.3,
            marker=dict(
                color='gray',
                )
            )
    )
    
    fig2 = px.scatter(n_df, x="x", y="y", color="cluster_name_map")


    fig.show()
    fig2.show()
    fig1.show()
    
```

```python pycharm={"is_executing": true}
def print_metrics(y_to_pred, y_pred, y_num, X):
    print('Метрики для размеченных данных')
    print('ARI',  metrics.adjusted_rand_score(y_to_pred, y_pred))
    print('AMI', metrics.adjusted_mutual_info_score(y_to_pred, y_pred))
    print('Homogenity', metrics.homogeneity_score(y_to_pred, y_pred))
    print('Completeness', metrics.completeness_score(y_to_pred, y_pred))
    print('V-measure', metrics.v_measure_score(y_to_pred, y_pred))
    print()
    print('Метрики для оценки связности данных')
    print('Коэффициент силуэта', metrics.silhouette_score(X, y_num))
    print('Индекс Калински-Харабаса', metrics.calinski_harabasz_score(X, y_num))
    print('Индекс Дэвиса-Болдина', metrics.davies_bouldin_score(X, y_num))
```

```python pycharm={"is_executing": true}
def selecting(type: list[str], df: pd.DataFrame):
    df = df.loc[df['Type'].isin(type)]
    old_indexes = df.index
    df.index = pd.RangeIndex(0, len(df.index))
    df["Color"] = pd.factorize(df["Color"])[0]
    df["Type"] = pd.factorize(df["Type"])[0]
    df["Font_color"] = pd.factorize(df["Font_color"])[0]
    return df, old_indexes
```

```python pycharm={"is_executing": true}
def cluster_grid_search(algo, grid, y_to_pred, X):
    best_params = None
    best_metric = -1

    cluster = algo()
    for params in ParameterGrid(grid):
        cluster.set_params(**params)
        cluster.fit(X)
        y_num = cluster.labels_
        y_pred = [y_num[i] for i in y_to_pred.index]
        y_to_t_pred = y_to_pred['cluster_name'].tolist()
        metric = metrics.v_measure_score(y_to_t_pred, y_pred)

        if metric > best_metric:
            best_params = params
            best_metric = metric

    return best_params
```

```python
def map_vectors(cluster_vector: list, labeled_vector: list):
    res_dict = {}
    cluster_set = set(cluster_vector)
    for cluster_value in cluster_set:
        sublist = [labeled_vector[i] for i in [i for i, x in enumerate(cluster_vector) if x == cluster_value]]
        sublist = [x for x in copy(sublist) if not isinstance(x, float)]
        if len(sublist) > 0:
            lable_value = max(set(sublist), key=sublist.count)
            res_dict[cluster_value] = lable_value
        else:
            res_dict[cluster_value] = 'trash'
    res_list = [res_dict[i] for i in cluster_vector]
    return res_list
```

```python pycharm={"is_executing": true}
grid_optics = {'min_samples': range(2, 20, 1),
               'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}
grid_kmeans = {'algorithm': ['lloyd', 'elkan', 'auto', 'full'], 'n_clusters': range(5, 40)}
grid_dbscan = {'eps':np.arange(1, 5, 0.5), 'min_samples': range(1, 10), 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}
```

Считывание и первичная обработка файла

```python
# directory = 'processed_tables'
# new_df = pd.DataFrame()
# for entry in os.scandir(directory):
#     if entry.is_file():
#         excel_data_df = pd.read_excel(entry.path, sheet_name='Sheet1')
#         new_df = pd.concat([new_df, excel_data_df], ignore_index=True)
```

```python
new_df = pd.read_excel('processed_tables/new_CМР_Fusion.xlsx', sheet_name='Sheet1', index_col='Unnamed: 0')
```

```python
df = new_df.copy()
col_names = [str(i) for i in df.columns]
df.columns = col_names
df = df.drop(columns=['Content', 'Start_content', 'Row', 'Column', 'Relative_Id'])
```

```python
df
```

Выборка строковых данных

```python
str_df, str_old_indexes = selecting(['str', 'datetime.datetime', 'datetime.time'], df)
str_df.shape
```

```python
str_df
```

```python
str_y = str_df[["cluster_name"]]
str_y['cluster_name'].str.strip()
y_to_pred = str_y.loc[(pd.notna(str_y['cluster_name']))]
```

```python
X = str_df.drop(['cluster_name'], axis=1)
X = X.fillna(0)
```

```python
str_kmeans_params = cluster_grid_search(KMeans, grid_kmeans, y_to_pred, X)
str_kmeans_clustering = KMeans(**str_kmeans_params)
str_kmeans_clustering.fit(X)
```

```python
str_kmeans_y_num = str_kmeans_clustering.labels_
str_kmeans_y_pred = [str_kmeans_y_num[i] for i in y_to_pred.index]
str_kmeans_y_to_pred = y_to_pred['cluster_name'].tolist()

str_kmeans_y_num_map = map_vectors(str_kmeans_y_num, str_y['cluster_name'].tolist())
str_kmeans_y_pred_map = [str_kmeans_y_num_map[i] for i in y_to_pred.index]

print('\nkmeans')
plots(X, str_y, str_kmeans_y_num_map)
print_metrics(str_kmeans_y_to_pred, str_kmeans_y_pred_map, str_kmeans_y_num, X)

def print_metrics(y_to_pred, y_pred, y_num, X):
    print('Метрики для размеченных данных')
    print('ARI',  metrics.adjusted_rand_score(y_to_pred, y_pred))
    print('AMI', metrics.adjusted_mutual_info_score(y_to_pred, y_pred))
    print('Homogenity', metrics.homogeneity_score(y_to_pred, y_pred))
    print('Completeness', metrics.completeness_score(y_to_pred, y_pred))
    print('V-measure', metrics.v_measure_score(y_to_pred, y_pred))
    print()
    print('Метрики для оценки связности данных')
    print('Коэффициент силуэта', metrics.silhouette_score(X, y_num))
    print('Индекс Калински-Харабаса', metrics.calinski_harabasz_score(X, y_num))
    print('Индекс Дэвиса-Болдина', metrics.davies_bouldin_score(X, y_num))

```

```python
str_DBSCAN_params = cluster_grid_search(DBSCAN, grid_dbscan, y_to_pred, X)
str_DBSCAN_clustering = DBSCAN(**str_DBSCAN_params)
str_DBSCAN_clustering.fit(X)
```

```python
str_DBSCAN_y_num = str_DBSCAN_clustering.labels_
str_DBSCAN_y_pred = [str_DBSCAN_y_num[i] for i in y_to_pred.index]
str_DBSCAN_y_to_pred = y_to_pred['cluster_name'].tolist()

str_DBSCAN_y_num_map = map_vectors(str_DBSCAN_y_num, str_y['cluster_name'].tolist())
str_DBSCAN_y_pred_map = [str_DBSCAN_y_num_map[i] for i in y_to_pred.index]

print('\nDBSCAN')
plots(X, str_y, str_DBSCAN_y_num_map)
print_metrics(str_DBSCAN_y_to_pred, str_DBSCAN_y_pred_map, str_DBSCAN_y_num, X)

# print('\nDBSCAN')
# plots(X, y, str_DBSCAN_y_num)
# print_metrics(str_DBSCAN_y_to_pred, str_DBSCAN_y_pred, str_DBSCAN_y_num, X)
```

```python
str_OPTICS_params = cluster_grid_search(OPTICS, grid_optics, y_to_pred, X)
str_OPTICS_clustering = OPTICS(**str_OPTICS_params)
str_OPTICS_clustering.fit(X)
```

```python
str_OPTICS_y_num = str_OPTICS_clustering.labels_
str_OPTICS_y_pred = [str_OPTICS_y_num[i] for i in y_to_pred.index]
str_OPTICS_y_to_pred = y_to_pred['cluster_name'].tolist()

str_OPTICS_y_num_map = map_vectors(str_OPTICS_y_num, str_y['cluster_name'].tolist())
str_OPTICS_y_pred_map = [str_OPTICS_y_num_map[i] for i in y_to_pred.index]

print('\nOPTICS')
# plots(X, str_y, str_OPTICS_y_num_map)
plots_to_pres(X, str_y, str_OPTICS_y_num, str_OPTICS_y_num_map)
print_metrics(str_OPTICS_y_to_pred, str_OPTICS_y_pred_map, str_OPTICS_y_num, X)

# print('\nOPTICS')
# plots(X, str_y, str_OPTICS_y_num)
# print_metrics(str_OPTICS_y_to_pred, str_OPTICS_y_pred, str_OPTICS_y_num, X)
```

NUMBER DFS

```python
number_df, number_old_indexes = selecting(['int', 'float'], df)
number_df.shape
```

```python
number_y = number_df[["cluster_name"]]
number_y['cluster_name'].str.strip()
y_to_pred = number_y.loc[(pd.notna(number_y['cluster_name']))]
```

```python
X = number_df.drop(['cluster_name'], axis=1)
X = X.fillna(0)
```

```python
number_kmeans_params = cluster_grid_search(KMeans, grid_kmeans, y_to_pred, X)
number_kmeans_clustering = KMeans(**number_kmeans_params)
number_kmeans_clustering.fit(X)
```

```python
number_kmeans_y_num = number_kmeans_clustering.labels_
number_kmeans_y_pred = [number_kmeans_y_num[i] for i in y_to_pred.index]
number_kmeans_y_to_pred = y_to_pred['cluster_name'].tolist()

number_kmeans_y_num_map = map_vectors(number_kmeans_y_num, number_y['cluster_name'].tolist())
number_kmeans_y_pred_map = [number_kmeans_y_num_map[i] for i in y_to_pred.index]

print('\nkmeans')
plots(X, number_y, number_kmeans_y_num_map)
print_metrics(number_kmeans_y_to_pred, number_kmeans_y_pred_map, number_kmeans_y_num, X)

# print('\nkmeans')
# plots(X, y, number_kmeans_y_num)
# print_metrics(number_kmeans_y_to_pred, number_kmeans_y_pred, number_kmeans_y_num, X)
```

```python
number_DBSCAN_params = cluster_grid_search(DBSCAN, grid_dbscan, y_to_pred, X)
number_DBSCAN_clustering = DBSCAN(**number_DBSCAN_params)
number_DBSCAN_clustering.fit(X)
```

```python
number_DBSCAN_y_num = number_DBSCAN_clustering.labels_
number_DBSCAN_y_pred = [number_DBSCAN_y_num[i] for i in y_to_pred.index]
number_DBSCAN_y_to_pred = y_to_pred['cluster_name'].tolist()

number_DBSCAN_y_num_map = map_vectors(number_DBSCAN_y_num, number_y['cluster_name'].tolist())
number_DBSCAN_y_pred_map = [number_DBSCAN_y_num_map[i] for i in y_to_pred.index]

print('\nDBSCAN')
plots(X, number_y, number_DBSCAN_y_num_map)
print_metrics(number_DBSCAN_y_to_pred, number_DBSCAN_y_pred_map, number_DBSCAN_y_num, X)

# print('\nDBSCAN')
# plots(X, y, number_DBSCAN_y_num)
# print_metrics(number_DBSCAN_y_to_pred, number_DBSCAN_y_pred, number_DBSCAN_y_num, X)
```

```python
number_OPTICS_params = cluster_grid_search(OPTICS, grid_optics, y_to_pred, X)
number_OPTICS_clustering = OPTICS(**number_OPTICS_params)
number_OPTICS_clustering.fit(X)
```

```python
number_OPTICS_y_num = number_OPTICS_clustering.labels_
number_OPTICS_y_pred = [number_OPTICS_y_num[i] for i in y_to_pred.index]
number_OPTICS_y_to_pred = y_to_pred['cluster_name'].tolist()

number_OPTICS_y_num_map = map_vectors(number_OPTICS_y_num, number_y['cluster_name'].tolist())
number_OPTICS_y_pred_map = [number_OPTICS_y_num_map[i] for i in y_to_pred.index]

print('\nOPTICS')
# plots(X, number_y, number_OPTICS_y_num_map)
plots_to_pres(X, number_y, number_OPTICS_y_num, number_OPTICS_y_num_map)
print_metrics(number_OPTICS_y_to_pred, number_OPTICS_y_pred_map, number_OPTICS_y_num, X)

# print('\nOPTICS')
# plots(X, number_y, number_OPTICS_y_num)
# print_metrics(number_OPTICS_y_to_pred, number_OPTICS_y_pred, number_OPTICS_y_num, X)
```

NoneType Cells

```python
none_df, none_old_indexes = selecting(['NoneType'], df)
none_df
```

```python
none_y = none_df[["cluster_name"]]
none_y['cluster_name'].str.strip()
y_to_pred = none_y.loc[(pd.notna(none_y['cluster_name']))]
```

```python
X = none_df.drop(['cluster_name'], axis=1)
X = X.fillna(0)
```

```python pycharm={"is_executing": true}
none_kmeans_params = cluster_grid_search(KMeans, grid_kmeans, y_to_pred, X)
none_kmeans_clustering = KMeans(**none_kmeans_params)
none_kmeans_clustering.fit(X)
```

```python pycharm={"is_executing": true}
none_kmeans_y_num = none_kmeans_clustering.labels_
none_kmeans_y_pred = [none_kmeans_y_num[i] for i in y_to_pred.index]
none_kmeans_y_to_pred = y_to_pred['cluster_name'].tolist()

none_kmeans_y_num_map = map_vectors(none_kmeans_y_num, none_y['cluster_name'].tolist())
none_kmeans_y_pred_map = [none_kmeans_y_num_map[i] for i in y_to_pred.index]

print('\nkmeans')
plots(X, none_y, none_kmeans_y_num_map)
print_metrics(none_kmeans_y_to_pred, none_kmeans_y_pred_map, none_kmeans_y_num, X)

# print('\nkmeans')
# plots(X, y, none_kmeans_y_num)
# print_metrics(none_kmeans_y_to_pred, none_kmeans_y_pred, none_kmeans_y_num, X)
```

```python
none_DBSCAN_params = cluster_grid_search(DBSCAN, grid_dbscan, y_to_pred, X)
none_DBSCAN_clustering = DBSCAN(**none_DBSCAN_params)
none_DBSCAN_clustering.fit(X)
```

```python
none_DBSCAN_y_num = none_DBSCAN_clustering.labels_
none_DBSCAN_y_pred = [none_DBSCAN_y_num[i] for i in y_to_pred.index]
none_DBSCAN_y_to_pred = y_to_pred['cluster_name'].tolist()

none_DBSCAN_y_num_map = map_vectors(none_DBSCAN_y_num, none_y['cluster_name'].tolist())
none_DBSCAN_y_pred_map = [none_DBSCAN_y_num_map[i] for i in y_to_pred.index]

print('\nDBSCAN')
plots(X, none_y, none_DBSCAN_y_num_map)
print_metrics(none_DBSCAN_y_to_pred, none_DBSCAN_y_pred_map, none_DBSCAN_y_num, X)

# print('\nDBSCAN')
# plots(X, y, none_DBSCAN_y_num)
# print_metrics(none_DBSCAN_y_to_pred, none_DBSCAN_y_pred, none_DBSCAN_y_num, X)
```

```python
none_OPTICS_params = cluster_grid_search(OPTICS, grid_optics, y_to_pred, X)
none_OPTICS_clustering = OPTICS(**none_OPTICS_params)
none_OPTICS_clustering.fit(X)
```

```python
none_OPTICS_y_num = none_OPTICS_clustering.labels_
none_OPTICS_y_pred = [none_OPTICS_y_num[i] for i in y_to_pred.index]
none_OPTICS_y_to_pred = y_to_pred['cluster_name'].tolist()

none_OPTICS_y_num_map = map_vectors(none_OPTICS_y_num, none_y['cluster_name'].tolist())
none_OPTICS_y_pred_map = [none_OPTICS_y_num_map[i] for i in y_to_pred.index]

print('\nOPTICS')
# plots(X, none_y, none_OPTICS_y_num_map)
plots_to_pres(X, none_y, none_OPTICS_y_num, none_OPTICS_y_num_map)
print_metrics(none_OPTICS_y_to_pred, none_OPTICS_y_pred_map, none_OPTICS_y_num, X)

# print('\nOPTICS')
# plots(X, none_y, none_OPTICS_y_num)
# print_metrics(none_OPTICS_y_to_pred, none_OPTICS_y_pred, none_OPTICS_y_num, X)
```

```python

```
