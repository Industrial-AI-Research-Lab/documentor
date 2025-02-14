from typing import Iterator

import pandas as pd

from documentor.structuries.columns import ColumnType
from documentor.structuries.document import Document
from documentor.structuries.fragment import Fragment
from documentor.structuries.structure import StructureNode, DocumentStructure
from documentor.formats.excel.fragment import SheetFragment


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
        return self._data.copy()

    @staticmethod
    def row_from_fragment(frag: SheetFragment) -> pd.DataFrame:
        """
        Get a dataframe from a single fragment

        :param frag: Representation of a table cell.
        :type frag: SheetFragment
        """
        return pd.DataFrame(frag.to_dict())

    def add_fragment(self, frag: SheetFragment) -> None:
        """
        Add a fragment to a dataframe

        :param frag: Representation of a table cell.
        :type frag: SheetFragment
        """
        pd.concat([self._data, pd.DataFrame(frag.to_dict())], ignore_index=True)

    def set_row_type(self, row_type: pd.Series) -> None:
        """
        Set row type values.

        :param row_type: row type data
        :type row_type: Series
        """
        self._data['row_type'] = row_type

    def set_ground_truth(self, ground_truth: pd.Series) -> None:
        """
        Set ground_truth values.

        :param ground_truth: user markup data
        :type ground_truth: Series
        """
        self._data['ground_truth'] = ground_truth

    def set_label(self, label: pd.Series) -> None:
        """
        Set label values.

        :param label: algorithmic markup data
        :type label: Series
        """
        self._data['label'] = label
