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
        Parse file and return a pandas DataFrame with data about fragments.

        Args:
            path (str): Path to the file.

        Returns:
            pd.DataFrame: DataFrame with data about fragments.

        Raises:
            ExtensionException: If file extension is not supported.
            OSError: If file is not found or can't be opened.
        """
        pass
