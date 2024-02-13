from copy import copy
from sklearn.cluster import DBSCAN, OPTICS, KMeans
import numpy as np
import pandas as pd
from plotly import express as px, graph_objects as go
from sklearn import metrics
from sklearn.manifold import TSNE
from sklearn.model_selection import ParameterGrid
from enum import Enum


class AlgorithmType(Enum):
    """
    Possible variants of the clustering algorithm.
    """
    DBSCAN = DBSCAN()
    KMEANS = KMeans()
    OPTICS = OPTICS()


grid_optics = {'algo': OPTICS, 'params': {'min_samples': range(2, 20, 1),
                                          'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}}
grid_kmeans = {'algo': KMeans, 'params': {'algorithm': ['lloyd', 'elkan', 'auto', 'full'], 'n_clusters': range(5, 40)}}
grid_dbscan = {'algo': DBSCAN, 'params': {'eps': np.arange(1, 5, 0.5), 'min_samples': range(1, 10),
                                          'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}}


def print_metrics(y_to_pred: pd.DataFrame, y_pred: list[str], y_num: list[str], x: pd.DataFrame):
    """
    Outputs metrics of clustering results.

    :param y_to_pred: y-column marked up by the algorithm
    :type y_to_pred: DataFrame
    :param y_pred: y-column marked up by the user
    :type y_pred: list[str]
    :param y_num: numerically marked up y-column
    :type y_num: list[str]
    :param x: metadata of sheet cells
    :type x: DataFrame
    """
    print('Метрики для размеченных данных')
    print('Homogenity', metrics.homogeneity_score(y_to_pred, y_pred))
    print('Completeness', metrics.completeness_score(y_to_pred, y_pred))
    print('V-measure', metrics.v_measure_score(y_to_pred, y_pred))
    print()
    print('Метрика для оценки связности данных')
    print('Коэффициент силуэта', metrics.silhouette_score(x, y_num))


def plots(x: pd.DataFrame, y: pd.DataFrame, y_num: list):
    """
    Getting graphs of clustering results.

    :param x: metadata of sheet cells
    :type x: DataFrame
    :param y: user-defined markup (only marked)
    :type y: DataFrame
    :param y_num: fully marked up by the algorithm y-column
    :type y_num: list
    """
    X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3)
    qw = X_embedded.fit_transform(x)
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


def map_vectors(cluster_vector: list[int], labeled_vector: list[str | float]) -> [list[str], dict[int, str]]:
    """
    Comparison of algorithm markup and user markup.

    :param cluster_vector: algorithm markup list
    :type cluster_vector: list[int]
    :param labeled_vector: user markup list
    :type labeled_vector: labeled_vector: list[str | float]
    :return: fully marked up by the algorithm y-column, y-column marked up by the algorithm,
    dictionary of markup number and name comparisons
    :rtype: list[str], dict[int, str]
    """
    res_dict = {}
    cluster_set = set(cluster_vector)
    labeled_dict = {v: labeled_vector.count(v) for v in set(labeled_vector)}
    for cluster_value in cluster_set:
        sublist = [labeled_vector[i] for i in [i for i, x in enumerate(cluster_vector) if x == cluster_value]]
        sublist = [x for x in copy(sublist) if not isinstance(x, float)]
        if len(sublist) > 0:
            sub_dict = {sub: sublist.count(sub) for sub in set(sublist)}
            label_value = max(set(sublist), key=sublist.count)
            for k, v in sub_dict.items():
                if sub_dict[k] == labeled_dict[k] and sub_dict[k] != label_value:
                    res_dict[max(cluster_vector) + 1] = sub_dict[k]
            res_dict[cluster_value] = label_value
        else:
            res_dict[cluster_value] = 'trash'
    res_list = [res_dict[i] for i in cluster_vector]
    return res_list, res_dict


def cluster_grid_search(algo: AlgorithmType, grid: dict, y_to_pred: pd.DataFrame, x: pd.DataFrame) -> dict:
    """
    Selection of parameters for the clustering algorithm.

    :param algo: clusterization algorithm used
    :type x: AlgorithmType
    :param grid: a set of parameters for search
    :type x: dict
    :param y_to_pred: user-defined markup (only marked)
    :type y_to_pred: DataFrame
    :param x: metadata of sheet cells
    :type x: DataFrame
    :return: best parameters for the algorithm
    :rtype: dict
    """
    best_params = None
    best_metric = -1

    cluster = algo()
    for params in ParameterGrid(grid):
        cluster.set_params(**params)
        cluster.fit(x)
        y_num = cluster.labels_
        y_pred = [y_num[i] for i in y_to_pred.index]
        y_to_t_pred = y_to_pred['cluster_name'].tolist()
        metric = metrics.v_measure_score(y_to_t_pred, y_pred)

        if metric > best_metric:
            best_params = params
            best_metric = metric

    return best_params


def selecting(type: list[str], df: pd.DataFrame) -> [pd.DataFrame, list[int]]:
    """
    Selects cells of a certain data type.

    :param type: list of data types included in the dataset
    :type type: list[str]
    :param df: dataset describing the metadata of all cells in the worksheet
    :type df: DataFrame
    :return: df of define type ,cell indexes in the original dataset,
    :rtype: DataFrame, list[int]
    """
    df = df.loc[df['Type'].isin(type)]
    old_indexes = df.index
    df.index = pd.RangeIndex(0, len(df.index))
    df["Color"] = pd.factorize(df["Color"])[0]
    df["Type"] = pd.factorize(df["Type"])[0]
    df["Font_color"] = pd.factorize(df["Font_color"])[0]
    return df, old_indexes


def devide(df: pd.DataFrame, type: list[str]) -> [list[int], pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Prepares the dataset for clustering.

    :param df: dataset describing the metadata of all cells in the worksheet
    :type df: DataFrame
    :param type: list of data types included in the dataset
    :type type: list[str]
    :return: cell indexes in the original dataset, metadata of sheet cells, user-defined markup (all cells),
    user-defined markup (only marked)
    :rtype: [list[int], pd.DataFrame, pd.DataFrame, pd.DataFrame]
    """
    type_df, old_indexes = selecting(type, df)
    type_y = type_df[["cluster_name"]]
    type_y['cluster_name'].str.strip()
    type_y_to_pred = type_y.loc[(pd.notna(type_y['cluster_name']))]
    type_X = type_df.drop(['cluster_name'], axis=1)
    type_X = type_X.fillna(0)

    return old_indexes, type_X, type_y, type_y_to_pred
