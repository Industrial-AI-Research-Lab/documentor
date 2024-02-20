import pandas as pd

from sklearn import metrics
from sklearn.cluster import DBSCAN

from documentor.structuries.classifier import FragmentClassifier
from documentor.types.excel.label_data import SheetLabeledFragment
from documentor.types.excel.clustering import (print_metrics, plots, map_vectors, cluster_grid_search, devide,
                                               grid_optics, grid_kmeans, grid_dbscan, AlgorithmType, row_typing)
from documentor.types.excel.fragment import SheetFragment

SheetFragmentClassType = int | str


class SheetFragmentClassifier(FragmentClassifier):
    """
    Class for sheet format fragment classifier.
    """

    _dict_map: dict[int: str]
    _cluster_model = AlgorithmType

    def __init__(self, algo: AlgorithmType = DBSCAN, params=None):
        """
        Creating a classifier of cells in a sheet document.

        :param algo: clusterization algorithm used
        :type algo: AlgorithmType | None
        """
        if params is None:
            params = {'eps': 0.1, 'min_samples': 3}
        self._cluster_model = algo(**params)
        self._dict_map = {}

    def cluster(self, y_to_pred: pd.DataFrame, x: pd.DataFrame, y: pd.DataFrame) -> [list[str], list[str],
                                                                                     list[str], list[int], str]:
        """
        Choosing the best clustering algorithm and obtaining a dictionary
        with a comparison of user and algorithmic markup.

        :param y_to_pred: user-defined markup (only marked)
        :type y_to_pred: DataFrame
        :param x: metadata of sheet cells
        :type x: DataFrame
        :param y: user-defined markup (all cells)
        :type y: DataFrame
        :return: fully marked up by the algorithm y-column, y-column marked up by the algorithm,
        y-column marked up by the user, numerically marked up y-column,
        the name of the selected algorithm
        :rtype: [list[str], list[str], list[str], list[int], str]
        """
        v_measure = 0
        silhouette_koef = 0
        for grid in [grid_dbscan, grid_optics, grid_kmeans]:
            algo_params = cluster_grid_search(grid['algo'], grid['params'], y_to_pred, x)
            algo_clustering = grid['algo'](**algo_params)
            algo_clustering.fit(x)

            algo_y_num = algo_clustering.labels_
            algo_y_to_pred = y_to_pred['cluster_name'].tolist()

            algo_y_num_map, algo_dict_map = map_vectors(algo_y_num, y['cluster_name'].tolist())
            algo_y_pred_map = [algo_y_num_map[i] for i in y_to_pred.index]

            if metrics.v_measure_score(algo_y_to_pred, algo_y_pred_map) > v_measure:
                v_measure = metrics.v_measure_score(algo_y_to_pred, algo_y_pred_map)
                silhouette_koef = metrics.silhouette_score(x, algo_y_num)
                y_num_map = algo_y_num_map
                al_y_to_pred = algo_y_to_pred
                y_pred_map = algo_y_pred_map
                y_num = algo_y_num
                al = grid['algo'].__name__
                self._cluster_model = grid['algo'](**algo_params)
                self._dict_map = algo_dict_map
            elif (metrics.v_measure_score(algo_y_to_pred, algo_y_pred_map) == v_measure and
                  metrics.silhouette_score(x, algo_y_num) > silhouette_koef):
                silhouette_koef = metrics.silhouette_score(x, algo_y_num)
                y_num_map = algo_y_num_map
                al_y_to_pred = algo_y_to_pred
                y_pred_map = algo_y_pred_map
                y_num = algo_y_num
                al = grid['algo'].__name__
                self._cluster_model = grid['algo'](**algo_params)
                self._dict_map = algo_dict_map

        return y_num_map, al_y_to_pred, y_pred_map, y_num, al

    def print_result(self, df: pd.DataFrame, df_types: list[str], type: str) -> None:
        """
        Displays the markup results.

        :param df: dataset describing the metadata of all cells in the worksheet
        :type df: DataFrame
        :param df_types: list of data types included in the dataset
        :type df_types:list[str]
        :param type: the name of the dataset type for the user
        :type type: str
        """
        old_indexes, X, y, y_to_pred = devide(df, df_types)
        y_num_map, al_y_to_pred, y_pred_map, y_num, al = self.cluster(y_to_pred, X, y)
        print(f'\ntype: {type}, algorithm: {al}')
        plots(X, y, y_num_map)
        print_metrics(al_y_to_pred, y_pred_map, y_num, X)

    def devide_and_cluster(self, df: pd.DataFrame) -> None:
        """
        Divides the dataset into parts by type.
        Determines the appropriate clustering algorithm for each part.
        Marks up data that is not labeled in the custom markup.
        Displays the markup results.

        :param df: dataset describing the metadata of all cells in the worksheet
        :type df: DataFrame
        """
        col_names = [str(i) for i in df.columns]
        df.columns = col_names
        # df_copy = row_typing(df)
        df_copy = df.drop(columns=['Content', 'Start_content', 'Row', 'Relative_Id'])

        self.print_result(df_copy, ['str', 'datetime.datetime', 'datetime.time'], 'string')
        self.print_result(df_copy, ['int', 'float'], 'number')
        self.print_result(df_copy, ['NoneType'], 'none')

    def simple_classify(self, fragment: SheetFragment) -> SheetLabeledFragment:
        """
        Classify fragment to one of the simple types.

        :param fragment: fragment of document
        :type fragment: str
        :return: fragment of document with mark
        :rtype: SheetLabeledFragment
        """
        fragment_type = self.cluster_model.fit(fragment.fragment)
        classified_fragment = SheetLabeledFragment(fragment_type)
        return classified_fragment
