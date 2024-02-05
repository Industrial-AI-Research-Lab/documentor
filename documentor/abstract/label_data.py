from abc import ABC, abstractmethod
from dataclasses import dataclass

from documentor.abstract.document import Document
from documentor.abstract.fragment import Fragment

FragmentLabelType = int | str


@dataclass(frozen=True)
class LabeledFragment(Fragment, ABC):
    """
    Abstract class for labeled fragments of document.
    """
    @abstractmethod
    @property
    def label(self) -> FragmentLabelType:
        """
        Label of fragment.

        :return: the label
        :rtype: FragmentLabelType
        """
        pass


class LabeledDocument(Document, ABC):
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
