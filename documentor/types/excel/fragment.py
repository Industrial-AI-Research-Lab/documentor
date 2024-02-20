import pandas as pd

from documentor.structuries.fragment import Fragment


class SheetFragment(Fragment):
    """
    Class for fragments of sheet format document.
    Each fragment represents a cell of a sheet.
    """

    _needed_columns = ['Content', 'Start_content', 'Relative_Id', 'Type', 'Row', 'Column',
                       'Length', 'Vertically_merged', 'Horizontally_merged', 'Font_selection', 'Top_border',
                       'Bottom_border', 'Left_border', 'Right_border', 'Color', 'Font_color', 'Is_Formula']

    _value = pd.DataFrame()

    def __init__(self, data: list):
        """
        Creating a fragment describing a sheet cell.
        :param data: metadata of the cell
        :type data: list
        """
        self._value = pd.DataFrame(data=[data], columns=self._needed_columns)

    def __str__(self) -> str:
        """
        String representation of fragment's value.
        :return: value of fragment
        :rtype: str
        """
        return self.frag['Start_content'][0]

    @property
    def value(self) -> pd.DataFrame:
        return self._value
