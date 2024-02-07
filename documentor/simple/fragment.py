import pandas as pd

from documentor.abstract.document import Fragment
from documentor.semantic.preprocessing.lemmatization import lemmatize


class SimpleTokenizedFragment(Fragment):
    """
    Represents a token of simple fragment
    """
    data: list[str]

    def __init__(self, tokens, *args, **kwargs):
        """
        Initialize class
        :param token: one token
        """
        self.data = tokens

    def __str__(self, *args, **kwargs):
        return str(self.data)


class SimpleFragment(Fragment):
    """
    Represents a simple fragment of document

    """
    data: str

    def __init__(self, row, *args, **kwargs):
        self.data = row

    def __str__(self, *args, **kwargs):
        """
        Represents a simple fragment of document
        :return: str
        """
        return str(self.data)
