import pandas as pd

from documentor.abstract.fragment import Fragment


class SheetFragment(Fragment):
    """
    Abstract class for fragments of document.

    Each fragment represents a structural unit of a document,
    for example, a table cell, a log entry, a paragraph of a document with a string value and parameters.
    """

    COLUMNS = ['Content', 'Start_content', 'Relative_Id', 'Type', 'Row', 'Column',
                'Length', 'Vertically_merged', 'Horizontally_merged', 'Font_selection', 'Top_border',
                'Bottom_border', 'Left_border', 'Right_border', 'Color', 'Font_color', 'Is_Formula']

    fragment = pd.DataFrame()

    def __init__(self, data: list):
        self.frag = pd.DataFrame(data=[data], columns=self.COLUMNS)

    def __str__(self) -> str:
        """
        String representation of fragment's value.
        :return: value of fragment
        :rtype: str
        """
        return self.frag['Start_content'][0]