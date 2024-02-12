from documentor.sheets.document import SheetDocument
from documentor.sheets.fragment import SheetFragment

import pandas as pd

SheetFragmentLabelType = int | str


class SheetLabeledFragment(SheetFragment):
    """
    Abstract class for labeled fragments of document.
    """
    mark: SheetFragmentLabelType

    @property
    def label(self) -> SheetFragmentLabelType:
        """
        Label of fragment.

        :return: the label
        :rtype: FragmentLabelType
        """
        return self.mark


class SheetLabeledDocument(SheetDocument):
    """
    Abstract class for document with labeled fragments. Not all fragments of document must be labeled, but at least one.
    """
    marks = pd.Series()

    def labeled_fragments(self) -> list[SheetLabeledFragment]:
        """
        List of labeled fragments of document.
        :return: labeled fragments
        :rtype: list[LabeledFragment]
        """
        return self.marks.tolist()
