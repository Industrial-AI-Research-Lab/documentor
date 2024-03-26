from abc import ABC, abstractmethod

import pandas as pd
from overrides import overrides

from documentor.structuries.custom_types import LabelType
from documentor.structuries.document import Document


# TODO rewrite this class

class ClassifierModel(ABC):
    @overrides
    @abstractmethod
    def load(self):
        pass

    @overrides
    @abstractmethod
    def save(self):
        pass


class FragmentClassifier(ABC):
    """
    Abstract class for fragment classifier.
    """

    model: ClassifierModel

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

    # def hierarchy_classify(self, doc: Document) -> LabelType:
    #     """
    #     Classify fragments of the document with using hierarchy.
    #
    #     :param doc: the document
    #     :type doc: Document
    #     :return: series with types of fragments
    #     :rtype: pd.Series[LabelType]
    #     """
    #     pass
