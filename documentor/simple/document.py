import pandas as pd

from documentor.abstract.document import Document, Fragment

class SimpleDocument(Document):
    """
    A simple document
    :param data: The data from document
    :type data: list[Fragment]
    """
    data: list[Fragment] = []

    def __init__(self):
        ...

    @classmethod
    def from_df(cls, df: pd.DataFrame):
        ...
