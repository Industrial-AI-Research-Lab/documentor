from abc import ABC, abstractmethod

import pandas as pd

from documentor.structuries.custom_types import LabelType
from documentor.structuries.document import Document


# TODO rewrite this class

class FragmentClassifier(ABC):
    """
    Abstract class for fragment classifier.
    """

    @abstractmethod
    def classify_fragments(self, doc: Document) -> pd.Series:
        """
        Classify fragments of the document.

        :param doc: the document
        :type doc: Document
        :return: series with types of fragments
        :rtype: pd.Series[LabelType]
        """
        pass

    def hierarchy_classify(self, doc: Document) -> LabelType:
        """
        Classify fragments of the document with using hierarchy.

        :param doc: the document
        :type doc: Document
        :return: series with types of fragments
        :rtype: pd.Series[LabelType]
        """
        pass
