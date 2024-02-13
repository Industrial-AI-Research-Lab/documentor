from abc import ABC, abstractmethod

from documentor.abstract.fragment import Fragment

FragmentClassType = int


class FragmentClassifier(ABC):
    """
    Abstract class for fragment classifier.
    """
    @abstractmethod
    def simple_classify(self, fragment: Fragment) -> FragmentClassType:
        """
        Classify fragment to one of the simple types.

        :param fragment: fragment of document
        :type fragment: str
        :return: type of fragment
        :rtype: str
        """
        pass

    def hierarchy_classify(self, fragment: str, ) -> FragmentClassType:
        """
        Classify fragment to one of the types in the hierarchy.

        :param fragment: fragment of document
        :type fragment: str
        :return: type of fragment
        :rtype: str
        """
        pass