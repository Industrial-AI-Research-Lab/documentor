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

```python
import pandas as pd
import numpy as np
import os
import operator
from copy import copy
from sklearn.cluster import DBSCAN, OPTICS, KMeans
from sklearn import metrics
from sklearn.manifold import TSNE
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.model_selection import ParameterGrid
```

```python
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
def selecting(type: list[str], df: pd.DataFrame):
    df = df.loc[df['Type'].isin(type)]
    old_indexes = df.index
    df.index = pd.RangeIndex(0, len(df.index))
    df["Color"] = pd.factorize(df["Color"])[0]
    df["Type"] = pd.factorize(df["Type"])[0]
    return df, old_indexes
```

```python
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

```python
grid_optics = {'min_samples': range(2, 20, 1),
               'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}
grid_kmeans = {'algorithm': ['lloyd', 'elkan', 'auto', 'full'], 'n_clusters': range(5, 40)}
grid_dbscan = {'eps':np.arange(1, 5, 0.5), 'min_samples': range(1, 10), 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}
```

```python
new_df = pd.read_excel('processed_tables/new_5.xlsx', sheet_name='Sheet1', index_col='Unnamed: 0')
```

```python
df = new_df.copy()
col_names = [str(i) for i in df.columns]
df.columns = col_names
df = df.drop(columns=['Row', 'Column', 'Relative_Id', 'row_context', 'col_context', 'env_context', 'Content', 'Start_content'])
df = df.drop(columns = [str(i) for i in range(0, 20)])
# df['Content'] = [hash(i) for i in df['Content'].tolist()]
df["Color"] = pd.factorize(df["Color"])[0]
df["Type"] = pd.factorize(df["Type"])[0]
```

```python
df
```

```python
y = df[["cluster_name"]]
y['cluster_name'].str.strip()
y_to_pred = y.loc[(pd.notna(y['cluster_name']))]
```

```python
X = df.drop(['cluster_name'], axis=1)
X = X.fillna(0)
```

```python
kmeans_params = cluster_grid_search(KMeans, grid_kmeans, y_to_pred, X)
kmeans_clustering = KMeans(**kmeans_params)
kmeans_clustering.fit(X)
```

```python
kmeans_y_num = kmeans_clustering.labels_
kmeans_y_pred = [kmeans_y_num[i] for i in y_to_pred.index]
kmeans_y_to_pred = y_to_pred['cluster_name'].tolist()

print('\nkmeans')
plots(X, y, kmeans_y_num)
print_metrics(kmeans_y_to_pred, kmeans_y_pred, kmeans_y_num, X)
```

```python
DBSCAN_params = cluster_grid_search(DBSCAN, grid_dbscan, y_to_pred, X)
DBSCAN_clustering = DBSCAN(**DBSCAN_params)
DBSCAN_clustering.fit(X)
```

```python
DBSCAN_y_num = DBSCAN_clustering.labels_
DBSCAN_y_pred = [DBSCAN_y_num[i] for i in y_to_pred.index]
DBSCAN_y_to_pred = y_to_pred['cluster_name'].tolist()

print('\nDBSCAN')
plots(X, y, DBSCAN_y_num)
print_metrics(DBSCAN_y_to_pred, DBSCAN_y_pred, DBSCAN_y_num, X)
```

```python
OPTICS_params = cluster_grid_search(DBSCAN, grid_optics, y_to_pred, X)
OPTICS_clustering = OPTICS(**OPTICS_params)
OPTICS_clustering.fit(X)
```

```python
OPTICS_y_num = OPTICS_clustering.labels_
OPTICS_y_pred = [OPTICS_y_num[i] for i in y_to_pred.index]
OPTICS_y_to_pred = y_to_pred['cluster_name'].tolist()

print('\nOPTICS')
plots(X, y, OPTICS_y_num)
print_metrics(OPTICS_y_to_pred, OPTICS_y_pred, OPTICS_y_num, X)
```

```python

```
