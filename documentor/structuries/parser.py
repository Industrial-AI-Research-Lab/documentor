from abc import ABC, abstractmethod

import pandas as pd

from documentor.structuries.document import Document


class ExtensionException(Exception):
    """
    Exception for errors while parsing files.
    """
    pass


class DocumentParser(ABC):
    """
    An abstract class for primary document processing.
    """

    @abstractmethod
    def parse_file(self, path: str) -> pd.DataFrame:
        """
        Parse file and pandas DataFrame with data about fragments.

        :param path: path to file
        :type path: str
        :return: Document object
        :rtype: Document
        :raises ExtensionException: if file extension is not supported
        :raises OSError: if file is not found or can't be opened
        """
        pass
