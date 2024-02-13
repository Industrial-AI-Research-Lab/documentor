from documentor.types.excel.document import SheetDocument
from documentor.types.excel.fragment import SheetFragment

import pandas as pd

SheetFragmentLabelType = int | str


class SheetLabeledFragment(SheetFragment):
    """
    Class for tagged fragments of a sheet format document.
    """
    mark: SheetFragmentLabelType

    def __init__(self, mark: str):
        """
        Assigning a cluster to a sheet document fragment.
        :param mark: name of the assigned cluster
        :type mark: str
        """
        self.mark = mark
        self.fragment['cluster_name'] = mark

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
    Class for sheet format document with labeled fragments.
    Not all fragments of document must be labeled, but at least one.
    """
    marks = pd.Series()

    def labeled_fragments(self) -> list[SheetLabeledFragment]:
        """
        List of labeled fragments of document.
        :return: labeled fragments
        :rtype: list[LabeledFragment]
        """
        return self.marks.tolist()
