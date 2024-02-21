from abc import ABC, abstractmethod

from documentor.structuries.document import Document
from documentor.structuries.structure import StructureNode, DocumentStructure


class StructureFinder(ABC):
    """
    Abstract class for finding structure in the document.
    """

    @abstractmethod
    def find_structure(self, doc: Document) -> DocumentStructure:
        """
        Find structure in the document.

        :param doc: the document
        :type doc: Document
        :return: DocumentStructure object with structure of the document
        :rtype: DocumentStructure
        """
        pass
