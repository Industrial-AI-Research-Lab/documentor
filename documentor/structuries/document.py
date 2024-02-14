from abc import ABC, abstractmethod
from typing import Iterator

import pandas as pd

from documentor.structuries.fragment import Fragment


class DocumentParsingException(Exception):
    """
    Exception for errors while parsing document from csv.
    """
    pass


class Document(ABC):
    """
    Abstract class for documents of any type. Documents consist of fragments.
    """
    _data: pd.DataFrame
    _columns: dict[str, str] = {}

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
    def needed_columns(cls) -> dict[str, str]:
        """
        Return for class needed column names in df for initialization.

        :return: column names with description
        :rtype: dict[str, str]
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

    @property
    def data(self) -> pd.DataFrame:
        """
        Get the data of the document.

        :return: the data
        :rtype: pd.DataFrame
        """
        return self._data

    @abstractmethod
    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to pandas DataFrame.

        :return: pandas DataFrame with data about fragments
        :rtype: pd.DataFrame
        """
        pass


class TextDocument(Document):
    """
    Simple realization of document with string fragments.
    """
    _data: pd.DataFrame
    _columns: dict[str, str] = {
        'value': 'The text value of the fragment'
    }

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
        check_data_frame(data)
        columns = list[self._columns.keys()]
        if name_mapper is not None:
            check_dict_str_str(name_mapper)
            columns = [name_mapper[k] if k in name_mapper else k for k in self._columns.keys()]
        data = data[columns].copy()
        if name_mapper is not None:
            reversed_name_mapper = {v: k for k, v in name_mapper.items()}
            name_mapper = dict(zip(columns, columns)) | reversed_name_mapper
            data.rename(columns=name_mapper, inplace=True)
        self._data = data

    @classmethod
    def needed_columns(cls) -> dict[str, str]:
        """
        Get the list of necessary columns for creating Document with their descriptions.

        :return: list of pairs (column name, column description)
        :rtype: list[tuple[str, str]]
        """
        return cls._columns

    def build_fragments(self) -> list[TextFragment]:
        """
        List of fragments of Document.

        Note: If speed is important, it is preferable to use iter_rows() method.

        :return: list of fragments
        :rtype: list[TextFragment]
        """
        return [TextFragment(row['value']) for _, row in self._data.iterrows()]

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
