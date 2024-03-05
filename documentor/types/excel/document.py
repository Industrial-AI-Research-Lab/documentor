from typing import Iterator

import pandas as pd

from documentor.structuries.columns import ColumnType
from documentor.structuries.document import Document
from documentor.structuries.fragment import Fragment
from documentor.structuries.structure import StructureNode, DocumentStructure
from documentor.types.excel.fragment import SheetFragment


class SheetDocument(Document):
    """
    Class for sheet documents.
    """
    _data = pd.DataFrame()
    _columns: dict[str, ColumnType] = {field: ColumnType(type) for field, type in SheetFragment.param_types_dict().items()}
    _root: StructureNode | None = None
    _structure: DocumentStructure | None = None

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Create a dataset describing the metadata of all cells in the worksheet.
        :param df: metadata of all cells in the sheet
        :type df: DataFrame
        """
        self._data = df

    @property
    def build_fragments(self) -> list[SheetFragment]:
        """
        List of fragments of Document.

        :return: list of fragments
        :rtype: list[Fragment]
        """
        return [SheetFragment(**d) for d in self._data.to_dict('records')]

    def iter_all(self) -> Iterator[Fragment]:
        """
        Iterate over all fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[Fragment]
        """
        for fragment in self.build_fragments:
            yield fragment

    def iter_all_str(self) -> Iterator[str]:
        """
        Iterate over all values of fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[str]
        """
        for fragment in self.build_fragments:
            yield fragment.__str__()

    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to pandas DataFrame.

        :return: pandas DataFrame with data about fragments
        :rtype: pd.DataFrame
        """
        return self._data

    @staticmethod
    def row_from_fragment(frag: SheetFragment) -> pd.DataFrame:
        return pd.DataFrame(frag.to_dict())

    def add_fragment(self, frag: SheetFragment) -> None:
        pd.concat([self._data, pd.DataFrame(frag.to_dict())], ignore_index=True)

    def update_data(self, df: pd.DataFrame) -> pd.DataFrame:
        self._data = df
        return self._data
