from abc import ABC, abstractmethod
from typing import Iterator

import pandas as pd

from structuries.fragment import TextFragment, Fragment


class Document:
    """
    Interface for document with fragments.
    """
    _fragments: list[Fragment] = []

    def __init__(self, fragments: list[Fragment]):
        self._fragments = fragments

    def fragments(self) -> list[Fragment]:
        """
        List of fragments of the Document.

        Note:
            If speed is important, prefer using iter_rows().

        Returns:
            list[Fragment]: List of fragments.
        """
        return self._fragments

    def iter_fragments(self) -> Iterator[Fragment]:
        for fragment in self._fragments:
            yield fragment

    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame with data about fragments.
        """
        data = [f.__dict__() for f in self._fragments]
        return pd.DataFrame(data)
