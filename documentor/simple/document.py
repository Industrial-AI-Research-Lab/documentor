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
    _fragments: list[Fragment]

    def __init__(self, data: any):
        self._data = data

    def build_fragments(self) -> list[Fragment]:
        """
        List of fragments of Document.
        :return: list of fragments
        :rtype: list[Fragment]
        """
        if self._fragments is None:
            self._fragments = [SimpleFragment(d) for d in self._data.values.tolist()]
        return self._fragments
