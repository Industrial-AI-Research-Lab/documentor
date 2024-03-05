import pandas as pd

from sklearn import metrics
from sklearn.cluster import DBSCAN

from documentor.structuries.classifier import FragmentClassifier
from documentor.structuries.custom_types import LabelType
from documentor.types.excel.document import SheetDocument
from documentor.types.excel.clustering import (print_metrics, plots, map_vectors, cluster_grid_search, devide,
                                               grid_optics, grid_kmeans, grid_dbscan, AlgorithmType, row_typing)
from documentor.types.excel.fragment import SheetFragment

SheetFragmentClassType = int | str


class SheetClassifier(FragmentClassifier):
    """
    Class for sheet format fragment classifier.
    """

    _str_dict_map: dict[int: str]
    _str_cluster_model = AlgorithmType
    _number_dict_map: dict[int: str]
    _number_cluster_model = AlgorithmType
    _none_dict_map: dict[int: str]
    _none_cluster_model = AlgorithmType

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

    def cluster(self, df: pd.DataFrame, df_types: list[str]) -> [pd.DataFrame, str, AlgorithmType, dict]:
        """
        Choosing the best clustering algorithm and obtaining a dictionary
        with a comparison of user and algorithmic markup.

        :param df: dataset describing the metadata of all cells in the worksheet
        :type df: DataFrame
        :param df_types: list of data types included in the dataset
        :type df_types:list[str]
        :return: DataFrame with labeled infor,
        the name of the selected algorithm
        :rtype: [DataFrame, str, AlgorithmType, dict]
        """
        old_indexes, x, y, y_to_pred = devide(df, df_types)

        v_measure = 0
        for grid in [grid_dbscan, grid_optics, grid_kmeans]:
            algo_params = cluster_grid_search(grid['algo'], grid['params'], y_to_pred, x)
            algo_clustering = grid['algo'](**algo_params)
            algo_clustering.fit(x)

            algo_y_num = algo_clustering.labels_
            algo_y_to_pred = y_to_pred['ground_truth'].tolist()
            full_algo_labels = []
            for i in range(len(algo_y_num)):
                if i in y_to_pred.index:
                    full_algo_labels.append(y_to_pred['ground_truth'][0])
                else:
                    full_algo_labels.append(None)

            algo_y_num_map, algo_dict_map = map_vectors(algo_y_num, y['ground_truth'].tolist())
            algo_y_pred_map = [algo_y_num_map[i] for i in y_to_pred.index]
            user_labels = []
            algo_labels = []
            k = 0
            for i in range(len(algo_y_num)):
                if i in y_to_pred.index:
                    user_labels.append(algo_y_pred_map[k])
                    algo_labels.append(algo_y_to_pred[k])
                    k += 1
                else:
                    user_labels.append(None)
                    algo_labels.append(None)

            if metrics.v_measure_score(algo_y_to_pred, algo_y_pred_map) >= v_measure:
                x_ = x.copy()
                v_measure = metrics.v_measure_score(algo_y_to_pred, algo_y_pred_map)
                x_['full_algo_labels'] = full_algo_labels
                x_['algo_labels'] = algo_labels
                x_['user_labels'] = user_labels
                al = grid['algo'].__name__
                cluster_model = grid['algo'](**algo_params)
                dict_map = algo_dict_map
                x_['y'] = y
                x_['old_indexes'] = old_indexes
        return x_, al, cluster_model, dict_map

    @staticmethod
    def print_result(df: pd.DataFrame, algo: str) -> None:
        """
        Displays the markup results.

        :param document: SheetDocument with label information
        :type document: SheetDocument
        :param algo: the name of the dataset type for the user
        :type algo: str
        """
        # df = document.to_df()
        x = df.drop(columns=['y', 'full_algo_labels', 'algo_labels', 'user_labels'])
        print(f'\ntype: {type}, algorithm: {algo}')
        plots(x, df['y'], df['full_algo_labels'])
        print_metrics(df['algo_labels'], df['user_labels'])

    def document_cluster(self, df: pd.DataFrame) -> SheetDocument:
        """
        Divides the dataset into parts by type.
        Determines the appropriate clustering algorithm for each part.
        Marks up data that is not labeled in the custom markup.

        :param document: sheet document information
        :type document: SheetDocument with label information
        """
        # df = document.to_df()
        col_names = [str(i) for i in df.columns]
        df.columns = col_names
        df_copy = row_typing(df)
        df_copy = df_copy.drop(columns=['content', 'start_content', 'row', 'relative_id'])

        str_res_df, str_al, str_model, str_dict = self.cluster(df_copy, ['str', 'datetime.datetime', 'datetime.time'])
        self._str_cluster_model = str_model
        self._str_dict_map = str_dict
        number_res_df, number_al, number_model, number_dict = self.cluster(df_copy, ['int', 'float'])
        self._number_cluster_model = number_model
        self._number_dict_map = number_dict
        none_res_df, none_al, none_model, none_dict = self.cluster(df_copy, ['NoneType'])
        self._none_cluster_model = none_model
        self._none_dict_map = none_dict

        ret_df = pd.DataFrame()
        ret_df = pd.concat([ret_df, str_res_df], ignore_index=True)
        ret_df = pd.concat([ret_df, number_res_df], ignore_index=True)
        ret_df = pd.concat([ret_df, none_res_df], ignore_index=True)
        ret_df = ret_df.sort_values('old_indexes')

        # document.update_data(ret_df)
        return ret_df

    def classify_fragments(self, doc: SheetDocument) -> pd.Series:
        """
        Classify fragments of the document.

        :param doc: the SheetDocument
        :type doc: SheetDocument
        :return: series with types of fragments
        :rtype: pd.Series[LabelType]
        """
        pass

    def simple_classify(self, fragment: SheetFragment) -> SheetFragment:
        """
        Classify fragment to one of the simple types.

        :param fragment: fragment of document
        :type fragment: str
        :return: fragment of document with mark
        :rtype: SheetLabeledFragment
        """
        if fragment.type in ['str', 'datetime.datetime', 'datetime.time']:
            fragment_type = self._str_cluster_model.fit(fragment.value)
            fragment_name = self._str_dict_map[fragment_type]
        elif fragment.type in ['int', 'float']:
            fragment_type = self._number_cluster_model.fit(fragment.value)
            fragment_name = self._number_dict_map[fragment_type]
        else:
            fragment_type = self._none_cluster_model.fit(fragment.value)
            fragment_name = self._none_dict_map[fragment_type]
        fragment.label = fragment_type
        fragment.label_merged = fragment_name
        return fragment
