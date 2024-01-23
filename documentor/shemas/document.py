from abc import ABC, abstractmethod
from typing import Iterator

import pandas as pd


class DocumentParsingException(Exception):
    pass


class Fragment(ABC):
    """
    Abstract class for fragments of document.

    Each fragment represents a structural unit of a document,
    for example, a table cell, a log entry, a paragraph of a document with a string value and parameters.
    """

    @abstractmethod
    def __str__(self) -> str:
        """
        String representation of fragment's value.
        :return: value of fragment
        :rtype: str
        """
        pass


class Document(ABC):
    """
    Abstract class for documents of any type. Documents consist of fragments.
    """

    @property
    @abstractmethod
    def fragments(self) -> list[Fragment]:
        """
        List of fragments of Document.
        :return: list of fragments
        :rtype: list[Fragment]
        """
        pass

    def iterall(self) -> Iterator[Fragment]:
        """
        Iterate over all fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[Fragment]
        """
        for fragment in self.fragments:
            yield fragment

    def iterall_str(self) -> Iterator[str]:
        """
        Iterate over all values of fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[str]
        """
        for fragment in self.fragments:
            yield fragment.__str__()

    @classmethod
    @abstractmethod
    def from_df(cls, df: pd.DataFrame) -> 'Document':
        """
        Create Document from pandas DataFrame.

        :param df: DataFrame with data about fragments
        :type df: pd.DataFrame
        :return: Document object
        :rtype: Document
        :raises DocumentParsingException: if DataFrame is not valid
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
