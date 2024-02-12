import pandas as pd
from sklearn.cluster import DBSCAN, OPTICS, KMeans
from sklearn import metrics

from documentor.abstract.classifier import FragmentClassifier
from documentor.sheets.clustering import (print_metrics, plots, map_vectors, cluster_grid_search, devide, grid_optics,
                                          grid_kmeans, grid_dbscan)
from documentor.sheets.fragment import SheetFragment

SheetFragmentClassType = int | str


class SheetFragmentClassifier(FragmentClassifier):
    """
    Abstract class for fragment classifier.
    """
    cluster_model = DBSCAN(eps=0.1, min_samples=3)
    dict_map: dict[int: str] = {}

    def cluster(self, y_to_pred, X, y):
        v_measure = 0
        silhouette_koef = 0
        for grid_params, algo in {grid_dbscan: DBSCAN, grid_optics: OPTICS, grid_kmeans: KMeans}:
            algo_params = cluster_grid_search(algo, grid_params, y_to_pred, X)
            algo_clustering = KMeans(**algo_params)
            algo_clustering.fit(X)

            algo_y_num = algo_clustering.labels_
            algo_y_to_pred = y_to_pred['cluster_name'].tolist()

            algo_y_num_map, algo_dict_map = map_vectors(algo_y_num, y['cluster_name'].tolist())
            algo_y_pred_map = [algo_y_num_map[i] for i in y_to_pred.index]

            if metrics.v_measure_score(y_to_pred, algo_y_pred_map) > v_measure:
                v_measure = metrics.v_measure_score(y_to_pred, algo_y_pred_map)
                silhouette_koef = metrics.silhouette_score(X, algo_y_num)
                y_num_map = algo_y_num_map
                al_y_to_pred = algo_y_to_pred
                y_pred_map = algo_y_pred_map
                y_num = algo_y_num
                al = algo.__name__
                self.cluster_model = algo(algo_params)
                self.dict_map = algo_dict_map
            elif (metrics.v_measure_score(y_to_pred, algo_y_pred_map) == v_measure and
                  metrics.silhouette_score(X, algo_y_num) > silhouette_koef):
                silhouette_koef = metrics.silhouette_score(X, algo_y_num)
                y_num_map = algo_y_num_map
                al_y_to_pred = algo_y_to_pred
                y_pred_map = algo_y_pred_map
                y_num = algo_y_num
                al = algo.__name__
                self.cluster_model = algo(algo_params)
                self.dict_map = algo_dict_map

        return y_num_map, al_y_to_pred, y_pred_map, y_num, al

    def result_output(self, df: pd.DataFrame, df_types: list(str), type: str):
        old_indexes, X, y, y_to_pred = devide(df, df_types)
        y_num_map, al_y_to_pred, y_pred_map, y_num, al = self.cluster(y_to_pred, X, y)
        print(type, al + '\n')
        print(f'type: {type}, algorithm: {al}')
        plots(X, y, y_num_map)
        print_metrics(al_y_to_pred, y_pred_map, y_num, X)

    def devide_and_cluster(self, df: pd.DataFrame):
        col_names = [str(i) for i in df.columns]
        df.columns = col_names
        df = df.drop(columns=['Content', 'Start_content', 'Row', 'Relative_Id'])

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
        fragment_type = self.cluster_model.fit(fragment.fragment)
        return self.dict_map[fragment_type]

    def hierarchy_classify(self, fragment: str) -> SheetFragmentClassType:
        """
        Classify fragment to one of the types in the hierarchy.

        :param fragment: fragment of document
        :type fragment: str
        :return: type of fragment
        :rtype: str
        """
        pass
