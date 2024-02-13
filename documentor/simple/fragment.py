import numpy as np
import pandas as pd

from documentor.abstract.document import Fragment
from documentor.semantic.preprocessing.lemmatization import lemmatize as get_lemas
from documentor.semantic.preprocessing.tokenization import tokenize as get_tokens

from documentor.semantic.models.base import BaseSemanticModel


class SimpleTokenizedFragment(Fragment):
    """
    Represents a fragment with tokens
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


class SimpleVectorizedFragment(Fragment):
    """
    Represents a fragment with vectors
    """
    data: np.ndarray

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
    tokens: np.ndarray | None
    lemas: list[str] | None

    def __init__(self, row, *args, **kwargs):
        self.data = row

    def __str__(self, *args, **kwargs):
        """
        Represents a simple fragment of document
        :return: str
        """
        return str(self.data)
