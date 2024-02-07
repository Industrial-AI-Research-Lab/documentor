import pandas as pd

from documentor.abstract.document import Document
from documentor.abstract.fragment import Fragment
from documentor.simple.fragment import SimpleFragment, SimpleTokenizedFragment
from documentor.semantic.preprocessing.lemmatization import lemmatize


class SimpleDocument(Document):
    """
    A simple document
    :param data: The data from document
    :type data: list[Fragment]
    """
    row_data: list[SimpleFragment]
    tokens: list[SimpleTokenizedFragment]

    def __init__(self, data: list[str]) -> None:
        self.row_data = [SimpleFragment(k) for k in data]

    @classmethod
    def from_df(cls, df: pd.DataFrame, target_column: str | None = None,
                *args, **kwargs) -> 'SimpleDocument':
        """
        Validate dataframe and transform it into a simple document
        :param df: pandas DataFrame with data
        :type df: pd.DataFrame
        :param target_column: Column name from which the text will be extracted
        :type target_column: str
        :return: SimpleDocument object
        :rtype: SimpleDocument
        """
        if target_column is None:
            target_column = df.columns[0]

        new_instance = SimpleDocument()
        new_instance.row_data = [SimpleFragment(k) for k in df[target_column].values.tolist()]

        return new_instance

    @property
    def fragments(self) -> list[Fragment]:
        return self.row_data

    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.row_data)

    def lemmatize(self, *args, **kwargs):
        """
        text partitioning into lemmatized tokens
        :return: None
        :rtype: None
        """
        self.tokens = [SimpleTokenizedFragment(lemmatize(row, args, kwargs))
                       for row in [str(d) for d in self.row_data]]
