from typing import Iterator

import pandas as pd

from documentor.structuries.document import Document
from documentor.structuries.fragment import Fragment
from documentor.types.excel.fragment import SheetFragment


class SheetDocument(Document):
    """
    Class for sheet documents.
    """
    _data = pd.DataFrame(columns=['Content', 'Start_content', 'Relative_Id', 'Type', 'Row', 'Column',
                                   'Length', 'Vertically_merged', 'Horizontally_merged', 'Font_selection', 'Top_border',
                                   'Bottom_border', 'Left_border', 'Right_border', 'Color', 'Is_Formula'])

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
        return self._data.to_list()

    def iter_all(self) -> Iterator[Fragment]:
        """
        Iterate over all fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[Fragment]
        """
        for fragment in self.fragments:
            yield fragment

    def iter_all_str(self) -> Iterator[str]:
        """
        Iterate over all values of fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[str]
        """
        for fragment in self.fragments:
            yield fragment.__str__()

    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to pandas DataFrame.

        :return: pandas DataFrame with data about fragments
        :rtype: pd.DataFrame
        """
        return self._data
