import pandas as pd

from documentor.structuries.document import Document
from documentor.structuries.fragment import Fragment
from documentor.simple.fragment import SimpleFragment

from documentor.semantic.models.base import BaseSemanticModel


class SimpleDocument(Document):
    """
    A simple document
    :param _data: The data from document
    :type _data: pd.DataFrame
    """
    _fragments: list[SimpleFragment]

    def __init__(self, data: any):
        self._data = data
        self._fragments = None

    def build_fragments(self) -> list[Fragment]:
        """
        List of fragments of Document.
        :return: list of fragments
        :rtype: list[Fragment]
        """
        if self._fragments is None:
            self._fragments = [SimpleFragment(d[0]) for d in self._data.values]
        return self._fragments
    
    def find_terms(self) -> set[str]:
        """
        Find specialized terms in fragments
        :return: set of finding terms
        :rtype: set[str]
        """
        return set([word for fragment in self._fragments for word in fragment.find_terms()])

    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to DataFrame
        :return: DataFrame of Document
        :rtype: pd.DataFrame
        """
        return self._data.copy()
