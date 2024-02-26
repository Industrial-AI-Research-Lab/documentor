import pandas as pd

from documentor.structuries.document import Document
from documentor.structuries.fragment import Fragment
from documentor.types.text.fragment import SimpleFragment


class SimpleDocument(Document):
    """
    A simple document
    :param _data: The data from document
    :type _data: pd.DataFrame
    """

    def __init__(self, data: pd.DataFrame, name_mapper: dict[str, str] | None = None):
        """
        Initializes an instance of the class by pandas DataFrame. The DataFrame should contain column.

        :param data: A pandas DataFrame containing the data.
        :type data: pd.DataFrame
        :param name_mapper: A dictionary mapping column names in 'data' to new names. Default is None.
        :type name_mapper: dict[str, str]
        :return: None
        :raises TypeError: if the object is not pandas DataFrame or name_mapper is not dict[str, str] or None
        """


    def build_fragments(self) -> list[Fragment]:
        """
        List of fragments of Document.
        :return: list of fragments
        :rtype: list[Fragment]
        """
        return [SimpleFragment(d) for d in self._data.values]

    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to DataFrame
        :return: DataFrame of Document
        :rtype: pd.DataFrame
        """
        return self._data.copy()
