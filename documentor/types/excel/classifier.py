import pandas as pd
import pickle

from sklearn import metrics
from sklearn.cluster import DBSCAN

from documentor.structuries.classifier import FragmentClassifier, ClassifierModel
from documentor.types.excel.document import SheetDocument
from documentor.types.excel.clustering import (print_metrics, plots, map_vectors, cluster_grid_search_v_measure, devide,
                                               grid_optics, grid_kmeans, grid_dbscan, AlgorithmType, row_typing)
from documentor.types.excel.fragment import SheetFragment

SheetFragmentClassType = int | str

type_dict = {'str': ['str', 'datetime.datetime', 'datetime.time'], 'number': ['int', 'float'], 'none': ['NoneType']}


class SheetClassifierModel(ClassifierModel):
    dict_map: dict[int: str]
    model = AlgorithmType

    def __init__(self, dict_map: dict[int: str], model: AlgorithmType):
        self.dict_map = dict_map
        self.model = model

    def load(self, path: str):
        self.model = pickle.load(path+'model')
        self.dict_map = pickle.load(path+'dict')

    def save(self, path: str):
        pickle.dump(self.model, path+'model')
        pickle.dump(self.dict_map, path+'dict')

class SheetClassifier(FragmentClassifier):
    """
    Class for sheet format fragment classifier.
    """

    model_dict: [str, SheetClassifierModel]

    def __init__(self, algo: AlgorithmType | None = DBSCAN, params=None, types: list | None = None):
        """
        Creating a classifier of cells in a sheet document.

        :param algo: clusterization algorithm used
        :type algo: AlgorithmType | None
        """
        if algo is None:
            algo = DBSCAN
        if params is None:
            params = {'eps': 0.1, 'min_samples': 3}
        if types:
            for t in types:
                self.model_dict[t] = SheetClassifierModel(dict_map={}, model=algo(**params))

    def cluster(self, df: pd.DataFrame, type_name: str, df_types: list[str]) -> pd.DataFrame:
        """
        Choosing the best clustering algorithm and obtaining a dictionary
        with a comparison of user and algorithmic markup.

        :param df: dataset describing the metadata of all cells in the worksheet
        :type df: DataFrame
        :param type_name: type name
        :type type_name: str
        :param df_types: list of data types included in the dataset
        :type df_types:list[str]
        :return: DataFrame with labeled infor,
        the name of the selected algorithm
        :rtype: DataFrame
        """
        old_indexes, x, y, y_to_pred = devide(df, df_types)

        v_measure = 0
        for grid in [grid_dbscan, grid_optics, grid_kmeans]:
            algo_params = cluster_grid_search_v_measure(grid['algo'], grid['params'], y_to_pred, x)
            algo_clustering = grid['algo'](**algo_params)
            algo_clustering.fit(x)

            algo_y_num = algo_clustering.labels_
            algo_y_to_pred = y_to_pred['ground_truth'].tolist()

            algo_y_num_map, algo_dict_map = map_vectors(algo_y_num, y['ground_truth'].tolist())
            algo_y_pred_map = [algo_y_num_map[i] for i in y_to_pred.index]

            if metrics.v_measure_score(algo_y_to_pred, algo_y_pred_map) >= v_measure:
                x_ = x.copy()
                v_measure = metrics.v_measure_score(algo_y_to_pred, algo_y_pred_map)
                x_['ground_truth'] = y
                x_['old_indexes'] = old_indexes
                x_['label'] = algo_y_num_map

                self.model_dict[type_name] = SheetClassifierModel(dict_map=algo_dict_map, model=algo_clustering)
        return x_

    @staticmethod
    def print_result(document: SheetDocument) -> None:
        """
        Displays the markup results.

        :param document: SheetDocument with label information
        :type document: SheetDocument
        """
        df = document.to_df()
        df = row_typing(df)
        df = df.drop(columns=['value', 'start_content', 'row', 'relative_id'])
        for n, t in type_dict.items():
            old_indexes, x, y, y_to_pred = devide(df, t)
            label = x['label'].to_list()
            label_to_pred = [label[i] for i in y_to_pred.index]
            x = x.drop(columns=['label'])
            print(f'Value type: {n}')
            plots(x, y, label)
            print_metrics(y_to_pred['ground_truth'].to_list(), label_to_pred)

    def classify_fragments(self, doc: SheetDocument) -> [pd.Series, SheetDocument]:
        """
        Classify fragments of the document.

        :param doc: the SheetDocument
        :type doc: SheetDocument
        :return: series with types of fragments
        :rtype: pd.Series[LabelType]
        """
        df = doc.to_df()
        df = row_typing(df)
        df = df.drop(columns=['value', 'start_content', 'row', 'relative_id'])
        ret_df = pd.DataFrame()
        for t, lst in type_dict.items():
            ret_df = pd.concat([ret_df, self.cluster(df, t, lst)], ignore_index=True)

        ret_df = ret_df.set_index('old_indexes')
        doc.set_label(ret_df['label'])
        doc.set_row_type(ret_df['row_type'])
        return ret_df['label'].sort_index(), doc

    def simple_classify(self, fragment: SheetFragment) -> SheetFragment:
        """
        Classify fragment to one of the simple types.

        :param fragment: fragment of document
        :type fragment: str
        :return: fragment of document with mark
        :rtype: SheetLabeledFragment
        """

        for t, lst in type_dict.items():
            if fragment.type in lst:
                fragment_type = self.model_dict[t].model.fit(fragment.value)
                fragment_name = self.model_dict[t].dict_map[fragment_type]

                fragment.label = fragment_type
                fragment.label_merged = fragment_name
        return fragment
