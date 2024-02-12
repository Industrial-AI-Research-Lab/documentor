from sklearn.model_selection import ParameterGrid
import pandas as pd
from sklearn.cluster import DBSCAN, OPTICS, KMeans
from sklearn import metrics
from sklearn.manifold import TSNE
import plotly.express as px
import plotly.graph_objects as go
from copy import copy
import numpy as np

from documentor.abstract.classifier import FragmentClassifier
from documentor.sheets.fragment import SheetFragment

SheetFragmentClassType = int


class SheetFragmentClassifier(FragmentClassifier):
    """
    Abstract class for fragment classifier.
    """
    grid_optics = {'min_samples': range(2, 20, 1),
                   'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}
    grid_kmeans = {'algorithm': ['lloyd', 'elkan', 'auto', 'full'], 'n_clusters': range(5, 40)}
    grid_dbscan = {'eps': np.arange(1, 5, 0.5), 'min_samples': range(1, 10),
                   'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}

    def selecting(self, type: list[str], df: pd.DataFrame):
        df = df.loc[df['Type'].isin(type)]
        old_indexes = df.index
        df.index = pd.RangeIndex(0, len(df.index))
        df["Color"] = pd.factorize(df["Color"])[0]
        df["Type"] = pd.factorize(df["Type"])[0]
        df["Font_color"] = pd.factorize(df["Font_color"])[0]
        return df, old_indexes

    def cluster_grid_search(self, algo, grid, y_to_pred, X):
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

    def map_vectors(self, cluster_vector: list, labeled_vector: list):
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

    def plots(self, X, y, y_num):
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

    def print_metrics(self, y_to_pred, y_pred, y_num, X):
        print('Метрики для размеченных данных')
        print('ARI', metrics.adjusted_rand_score(y_to_pred, y_pred))
        print('AMI', metrics.adjusted_mutual_info_score(y_to_pred, y_pred))
        print('Homogenity', metrics.homogeneity_score(y_to_pred, y_pred))
        print('Completeness', metrics.completeness_score(y_to_pred, y_pred))
        print('V-measure', metrics.v_measure_score(y_to_pred, y_pred))
        print()
        print('Метрики для оценки связности данных')
        print('Коэффициент силуэта', metrics.silhouette_score(X, y_num))
        print('Индекс Калински-Харабаса', metrics.calinski_harabasz_score(X, y_num))
        print('Индекс Дэвиса-Болдина', metrics.davies_bouldin_score(X, y_num))

    def cluster(self, y_to_pred, X, y):
        v_measure = 0
        silhouette_koef = 0
        for grid_params, algo in {self.grid_dbscan: DBSCAN, self.grid_optics: OPTICS, self.grid_kmeans: KMeans}:
            algo_params = self.cluster_grid_search(algo, grid_params, y_to_pred, X)
            algo_clustering = KMeans(**algo_params)
            algo_clustering.fit(X)

            algo_y_num = algo_clustering.labels_
            algo_y_to_pred = y_to_pred['cluster_name'].tolist()

            algo_y_num_map = self.map_vectors(algo_y_num, y['cluster_name'].tolist())
            algo_y_pred_map = [algo_y_num_map[i] for i in y_to_pred.index]

            if metrics.v_measure_score(y_to_pred, algo_y_pred_map) > v_measure:
                v_measure = metrics.v_measure_score(y_to_pred, algo_y_pred_map)
                silhouette_koef = metrics.silhouette_score(X, algo_y_num)
                y_num_map = algo_y_num_map
                al_y_to_pred = algo_y_to_pred
                y_pred_map = algo_y_pred_map
                y_num = algo_y_num
                al = algo.__name__
            elif (metrics.v_measure_score(y_to_pred, algo_y_pred_map) == v_measure and
                  metrics.silhouette_score(X, algo_y_num) > silhouette_koef):
                silhouette_koef = metrics.silhouette_score(X, algo_y_num)
                y_num_map = algo_y_num_map
                al_y_to_pred = algo_y_to_pred
                y_pred_map = algo_y_pred_map
                y_num = algo_y_num
                al = algo.__name__

        return y_num_map, al_y_to_pred, y_pred_map, y_num, al

    def devide(self, df: pd.DataFrame, type: list(str)):
        type_df, old_indexes = self.selecting(type, df)
        type_y = type_df[["cluster_name"]]
        type_y['cluster_name'].str.strip()
        type_y_to_pred = type_y.loc[(pd.notna(type_y['cluster_name']))]
        type_X = type_df.drop(['cluster_name'], axis=1)
        type_X = type_X.fillna(0)

        return old_indexes, type_X, type_y, type_y_to_pred

    def result_output(self, df: pd.DataFrame, df_types: list(str), type: str):
        old_indexes, X, y, y_to_pred = self.devide(df, df_types)
        y_num_map, al_y_to_pred, y_pred_map, y_num, al = self.cluster(y_to_pred, X, y)
        print(type, al + '\n')
        print(f'type: {type}, algorithm: {al}')
        self.plots(X, y, y_num_map)
        self.print_metrics(al_y_to_pred, y_pred_map, y_num, X)

    def devide_and_cluster(self, df: pd.DataFrame):
        col_names = [str(i) for i in df.columns]
        df.columns = col_names
        df = df.drop(columns=['Content', 'Start_content', 'Row', 'Column', 'Relative_Id'])

        self.result_output(df, ['str', 'datetime.datetime', 'datetime.time'], 'string')
        self.result_output(df, ['int', 'float'], 'number')
        self.result_output(df, ['none'], 'none')

    def simple_classify(self, fragment: SheetFragment) -> SheetFragmentClassType:
        """
        Classify fragment to one of the simple types.

        :param fragment: fragment of document
        :type fragment: str
        :return: type of fragment
        :rtype: str
        """
        pass

    def hierarchy_classify(self, fragment: str) -> SheetFragmentClassType:
        """
        Classify fragment to one of the types in the hierarchy.

        :param fragment: fragment of document
        :type fragment: str
        :return: type of fragment
        :rtype: str
        """
        pass
