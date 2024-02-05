from abc import ABC, abstractmethod
from dataclasses import dataclass

from documentor.abstract.document import Document


class ExtensionException(Exception):
    """
    Exception for errors while parsing files.
    """
    pass


@dataclass(frozen=True)
class SimpleParser(ABC):
    @abstractmethod
    def from_file(self, path: str) -> Document:
        """
        Create Document from file.

        :param path: path to file
        :type path: str
        :return: Document object
        :rtype: Document
        :raises ExtensionException: if file extension is not supported
        :raises DocumentParsingException: if file structure is not valid
        :raises OSError: if file is not found or can't be opened
        """
        pass

    @abstractmethod
    def from_csv(self, path: str, sep: str | None) -> Document:
        """
        Create Document from pandas DataFrame.

        :param path: path to file
        :param sep: separator for csv file
        :return: Document object
        :rtype: Document
        :raises DocumentParsingException: if csv structure is not valid
        :raises OSError: if file is not found or can't be opened
        """
        pass

    @abstractmethod
    def to_file(self, document: Document, path: str, extension: str | None):
        """
        Save Document to file.

        :param document: Document object for storing in file
        :type document: Document
        :param path: path to file
        :type path: str
        :param extension: extension of file
        :return:
        :raises ExtensionException: if file extension is not supported
        :raises OSError: if document can't be written to file
        """
        pass

    @abstractmethod
    def to_csv(self, document: Document, sep: str | None):
        """
        Save Document to csv file.

        :param document: Document object for storing in csv file
        :type document: Document
        :param sep: separator for csv file
        :type sep: str
        :return:
        :raises OSError: if document can't be written to file
        """
        pass
