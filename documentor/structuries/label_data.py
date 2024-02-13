from abc import ABC, abstractmethod
from dataclasses import dataclass

from documentor.structuries.document import Document
from documentor.structuries.fragment import Fragment

FragmentLabelType = int | str


class LabeledFragment(FragmentWrapper):
    """
    Abstract class for labeled fragments of document.
    """
    _label: FragmentLabelType

    def __init__(self, fragment: FragmentInterface, label: FragmentLabelType) -> None:
        self._fragment = fragment
        self._label = label

    @property
    def label(self) -> FragmentLabelType:
        """
        Label of fragment.

        :return: the label
        :rtype: FragmentLabelType
        """
        return self._label


class LabeledDocument(TextDocument, ABC):
    """
    Abstract class for document with labeled fragments. Not all fragments of document must be labeled, but at least one.
    """

    @abstractmethod
    def labeled_fragments(self) -> list[LabeledFragment]:
        """
        List of labeled fragments of document.
        :return: labeled fragments
        :rtype: list[LabeledFragment]
        """
        pass
