import pandas as pd

from documentor.abstract.document import Document
from documentor.simple.fragment import SimpleFragment

class SimpleDocument(Document):
    """
    A simple document
    :param data: The data from document
    :type data: list[Fragment]
    """
    data: list[SimpleFragment]

    def __init__(self):
        ...

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
        new_instance.data = [SimpleFragment(k) for k in df[target_column].values.tolist()]

        return new_instance

    def lemmatize(self, *args, **kwargs):
        """
        Lemmatize all fragments in data
        :return: None
        :rtype: None
        """
        for fragment in self.data:
            fragment.lemmatization(*args, **kwargs)
