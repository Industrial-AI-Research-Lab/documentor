from abc import ABC, abstractmethod

import pandas as pd

from documentor.structuries.document import Document


# TODO rewrite this class

class ClassifierModel(ABC):
    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def save_model(self):
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

        Args:
            doc (Document): The document to classify.

        Returns:
            pd.Series: Series with types of fragments.
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
