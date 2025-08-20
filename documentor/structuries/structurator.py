from abc import ABC, abstractmethod

from documentor.structuries.document import Document
from documentor.structuries.structure import DocumentStructure


class StructureFinder(ABC):
    """
    Abstract class for finding structure in the document.
    """

    @abstractmethod
    def find_structure(self, doc: Document) -> DocumentStructure:
        """
        Find structure in the document.

        Args:
            doc (Document): The document to analyze.

        Returns:
            DocumentStructure: Structure of the document.
        """
        pass
