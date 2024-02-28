from abc import ABC, abstractmethod
from typing import Iterator

import pandas as pd
from overrides import overrides

from documentor.structuries.columns import ColumnType
from documentor.structuries.fragment import Fragment

from documentor.structuries.type_check import check_data_frame, check_dict_str_str
from documentor.text.fragment import TextFragment

from documentor.structuries.structure import StructureNode, DocumentStructure
from documentor.structuries.type_check import TypeChecker as tc


class DocumentInterface(ABC):
    """
    Interface for document with fragments.
    """

    @abstractmethod
    def build_fragments(self) -> list[Fragment]:
        """
        List of fragments of Document.

        Note: if speed is important, it is preferable to use iter_rows method.

        :return: list of fragments
        :rtype: list[Fragment]
        """
        pass

    @abstractmethod
    def iter_rows(self) -> Iterator[tuple[int, pd.Series]]:
        """
        Iterate over all fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[str]
        """
        pass

    @abstractmethod
    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to pandas DataFrame.

        :return: pandas DataFrame with data about fragments
        :rtype: pd.DataFrame
        """
        pass


class Document(DocumentInterface):
    """
    Simple realization of document with string fragments.

    Document is a collection of fragments. Otherwise, document does not store fragments, it works with pd.DataFrame,
    which contain same column names as Fragment class field names.
    """
    _data: pd.DataFrame
    _columns: dict[str, ColumnType] = {field: ColumnType(type) for field, type in Fragment.param_types_dict().items()}
    _root: StructureNode | None = None
    _structure: DocumentStructure | None = None

    def __init__(self, data: pd.DataFrame):
        """
        Initializes an instance of the class by pandas DataFrame.

        The DataFrame should contain column names as Fragment class field names.
        Namely, it must contain one required field:
        - 'value' - value of the fragment.
        Also, it can contain optional fields, which will be used for initialization of the document:
        - 'ground_truth' - ground truth label of the fragment, if it is labeled
        - 'label' - label of the fragment from classification
        - 'vector' - vector representation of the fragment
        - 'tokens' - list of tokens of the fragment
        - 'token_vectors' - list of vectors of tokens of the fragment.
        """
        tc.check_data_frame_type(data)
        # tc.check_data_frame_columns(data, self._columns)
        columns = list[self._columns.keys()]
        self._data = data[columns].copy()

    @overrides
    def build_fragments(self) -> list[Fragment]:
        """
        List of fragments of Document.

        Note: If speed is important, it is preferable to use iter_rows() method.

        :return: list of fragments
        :rtype: list[TextFragment]
        """
        return [Fragment(**row.to_dict()) for _, row in self._data.iterrows()]

    @overrides
    def iter_rows(self) -> Iterator[tuple[int, pd.Series]]:
        """
        Iterate over all fragments of the Document with their row numbers.

        :return: the document fragments with their row numbers
        :rtype: Iterator[tuple[int, TextFragment]]
        """
        for i, row in self._data.iterrows():
            yield i, row

    @overrides
    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to pandas DataFrame.

        :return: pandas DataFrame with data about fragments
        :rtype: pd.DataFrame
        """
        return self._data.copy()

    @property
    def value(self) -> pd.Series:
        """
        Values of all fragments.

        :return: all values
        :rtype: pd.Series
        """
        return self._data['value']

    @property
    def ground_truth(self) -> pd.Series:
        """
        Ground truth labels of all fragments.

        :return: all ground truth labels
        :rtype: pd.Series
        """
        return self._data['ground_truth']

    @property
    def label(self) -> pd.Series:
        """
        Labels of all fragments.

        :return: all labels
        :rtype: pd.Series
        """
        return self._data['label']

    @label.setter
    def label(self, value: pd.Series) -> None:
        """
        Set labels of all fragments.

        :param value: new labels
        :type value: pd.Series
        :return: None
        :raises TypeError: value.dtype is not the same as Fragment.label type
        """
        # tc.check_series(value, self._columns['label'])
        self._data['label'] = value

    @property
    def vector(self) -> pd.Series:
        """
        Vector representations of all fragments.

        :return: all vector representations
        :rtype: pd.Series
        """
        return self._data['vector']

    @vector.setter
    def vector(self, value: pd.Series) -> None:
        """
        Set vector representations of all fragments.

        :param value: new vector representations
        :type value: pd.Series
        :return: None
        :raises TypeError: value.dtype is not the same as Fragment.vector type
        """
        # tc.check_series(value, self._columns['vector'])
        self._data['vector'] = value

    @property
    def tokens(self) -> pd.Series:
        """
        Tokens of all fragments.

        :return: all tokens
        :rtype: pd.Series
        """
        return self._data['tokens']

    @tokens.setter
    def tokens(self, value: pd.Series) -> None:
        """
        Set tokens of all fragments.

        :param value: new tokens
        :type value: pd.Series
        :return: None
        :raises TypeError: value.dtype is not the same as Fragment.tokens type
        """
        # tc.check_series(value, self._columns['tokens'])
        self._data['tokens'] = value

    @property
    def token_vectors(self) -> pd.Series:
        """
        Vectors of tokens of all fragments.

        :return: all token vectors
        :rtype: pd.Series
        """
        return self._data['token_vectors']

    @token_vectors.setter
    def token_vectors(self, value: pd.Series) -> None:
        """
        Set vectors of tokens of all fragments.

        :param value: new token vectors
        :type value: pd.Series
        :return: None
        :raises TypeError: value.dtype is not the same as Fragment.token_vectors type
        """
        # tc.check_series(value, self._columns['token_vectors'])
        self._data['token_vectors'] = value
