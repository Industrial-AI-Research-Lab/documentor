from copy import copy
from itertools import chain

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
    KMeans = KMeans()
    OPTICS = OPTICS()


grid_optics = {'algo': OPTICS, 'params': {'min_samples': range(2, 20, 1),
                                          'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}}
grid_kmeans = {'algo': KMeans, 'params': {'algorithm': ['lloyd', 'elkan', 'auto', 'full'], 'n_clusters': range(5, 40)}}
grid_dbscan = {'algo': DBSCAN, 'params': {'eps': np.arange(1, 5, 0.5), 'min_samples': range(1, 10),
                                          'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}}


def print_metrics(y_to_pred: pd.DataFrame, y_pred: list[str]):
    """
    Outputs metrics of clustering results.

    :param y_to_pred: y-column marked up by the algorithm
    :type y_to_pred: DataFrame
    :param y_pred: y-column marked up by the user
    :type y_pred: list[str]
    :param x: metadata of sheet cells
    :type x: DataFrame
    """
    print('Метрики для размеченных данных')
    print('Homogeneity', metrics.homogeneity_score(y_to_pred, y_pred))
    print('Completeness', metrics.completeness_score(y_to_pred, y_pred))
    print('V-measure', metrics.v_measure_score(y_to_pred, y_pred))


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
        y_to_t_pred = y_to_pred['ground_truth'].tolist()
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
    df = df.loc[df['type'].isin(type)]
    old_indexes = df.index
    df.index = pd.RangeIndex(0, len(df.index))
    df["color"] = pd.factorize(df["color"])[0]
    df["type"] = pd.factorize(df["type"])[0]
    df["font_color"] = pd.factorize(df["font_color"])[0]
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
    type_y = type_df[["ground_truth"]]
    type_y['ground_truth'].str.strip()
    type_y_to_pred = type_y.loc[(pd.notna(type_y['ground_truth']))]
    type_X = type_df.drop(['ground_truth'], axis=1)
    type_X = type_X.fillna(0)

    return old_indexes, type_X, type_y, type_y_to_pred


def row_typing(df: pd.DataFrame) -> pd.DataFrame:
    """
    The function of classifying table rows.

    :param df: dataset describing the metadata of all cells in the worksheet
    :type df: DataFrame
    :return: dataset describing the metadata of all cells in the worksheet with row tupes
    :rtype: DataFrame
    """
    ndf = df[['row', 'column', 'color', 'vertically_merged', 'horizontally_merged', 'font_selection', 'is_formula', 'type', 'font_color']]
    ndf["color"] = pd.factorize(ndf["color"])[0]
    ndf["type"] = pd.factorize(ndf["type"])[0]
    ndf["font_color"] = pd.factorize(ndf["font_color"])[0]
    ndf['row'] -= ndf['row'].iloc[0]
    ndf['column'] -= ndf['column'].iloc[0]
    ndf.reset_index(drop=True, inplace=True)

    arr = np.empty((ndf.tail(1)['row'].iloc[0] + 1, ndf.tail(1)['column'].iloc[0] + 1), dtype="object")
    for i, row in ndf.iterrows():
        arr[row['row'], row['column']] = row.values.tolist()
    mass = [list(chain.from_iterable([arr[i][j] for j in range(len(arr[i]))])) for i in range(len(arr))]
    rest_df = pd.DataFrame(data=mass)
    rest_df = rest_df.fillna(0)

    in_cols = []
    for i in rest_df.columns:
        if int(i) % 9 in [2, 3, 4, 5, 6, 7, 8]:
            in_cols.append(True)
        else:
            in_cols.append(False)

    rest_df = rest_df.iloc[:, in_cols]

    ald = DBSCAN().fit(rest_df)
    rest_df['labels'] = ald.labels_
    rest_df['labels'] = rest_df['labels'].apply(lambda x: x + 1)
    part_list = rest_df['labels']

    to_merge_df = pd.DataFrame()
    to_merge_df['row'] = rest_df.index + ndf['row'].iloc[0]
    to_merge_df['labels'] = part_list
    to_merge_df = to_merge_df.set_index('row')

    str_type_list = []
    names = list(df.columns)
    r_i = names.index('row') + 1
    for row in df.itertuples():
        a = to_merge_df['labels'][row[r_i]] if row[r_i] in list(to_merge_df.index) else None
        str_type_list.append(a)
    df['row_type'] = str_type_list
    return df