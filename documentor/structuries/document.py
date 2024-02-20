from abc import ABC, abstractmethod
from typing import Iterator

import pandas as pd

from documentor.structuries.columns import ColumnType
from documentor.structuries.fragment import Fragment
from documentor.structuries.type_check import TypeChecker as tc


class DocumentInterface(ABC):
    """
    Abstract class for documents of any type. Documents consist of fragments.


    """

    @abstractmethod
    def __init__(self, data: pd.DataFrame, name_mapper: dict[str, str] | None = None):
        """
        Initializes an instance of the class by pandas DataFrame. The DataFrame should contain column.

        :param data: A pandas DataFrame containing the data.
        :type data: pd.DataFrame
        :param name_mapper: A dictionary mapping column names in 'data' to new names. Default is None.
        :type name_mapper: dict[str, str]
        :return: None
        :raises TypeError: if the object is not pandas DataFrame or name_mapper is not dict[str, str] or None
        """
        pass

    @classmethod
    def _columns(cls) -> dict[str, bool, type]:
        """
        Return for class needed column names in df for initialization with their descriptions.

        :return: column names with description
        :rtype: dict[str, bool, str]
        """
        pass

    @abstractmethod
    def build_fragments(self) -> list[Fragment]:
        """
        List of fragments of Document.

        Note: if speed is important, it is preferable to use iter_rows method.

        :return: list of fragments
        :rtype: list[Fragment]
        """
        pass

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
    Simple realization of document with string fragments and mono class classification.
    """
    _data: pd.DataFrame
    _columns: dict[str, ColumnType] = {field: ColumnType(type) for field, type in Fragment.__annotations__.items()}

    def __init__(self, data: pd.DataFrame, name_mapper: dict[str, str] | None = None):
        """
        Initializes an instance of the class by pandas DataFrame.

        The DataFrame should contain next columns:
        - value: value of fragments.

        Optional columns that will be used in initialization if they are in DataFrame:
        - ground_truth: ground truth label of fragments.
        - label: label of fragments from classification.
        - vector: vector representation of fragments.
        - tokens: list of tokens of fragments.
        - token_vectors: list of vectors of tokens of fragments.

        :param data: A pandas DataFrame containing the data.
        :type data: pd.DataFrame
        :return: None
        :raises TypeError: if the object is not pandas DataFrame or name_mapper is not dict[str, str] or None
        :raises ValueError: if the DataFrame does not contain necessary columns
        """
        tc.check_data_frame_type(data)
        tc.check_data_frame_columns(data, self._columns)
        columns = list[self._columns.keys()]
        self._data = data[columns].copy()

    def build_fragments(self) -> list[Fragment]:
        """
        List of fragments of Document.

        Note: If speed is important, it is preferable to use iter_rows() method.

        :return: list of fragments
        :rtype: list[TextFragment]
        """
        return [Fragment(row['value']) for _, row in self._data.iterrows()]

    def iter_rows(self) -> Iterator[tuple[int, pd.Series]]:
        """
        Iterate over all fragments of the Document with their row numbers.

        :return: the document fragments with their row numbers
        :rtype: Iterator[tuple[int, TextFragment]]
        """
        for i, row in self._data.iterrows():
            yield i, row

    def iter_all_str(self) -> Iterator[str]:
        """
        Iterate over all values of fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[str]
        """
        for _, row in self.iter_rows():
            yield row['value']

    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to pandas DataFrame.

        :return: pandas DataFrame with data about fragments
        :rtype: pd.DataFrame
        """
        return self._data.copy()
