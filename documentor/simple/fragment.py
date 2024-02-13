import numpy as np
import pandas as pd

from documentor.structuries.document import Fragment
from documentor.semantic.preprocessing.lemmatization import lemmatize as get_lemas
from documentor.semantic.preprocessing.tokenization import tokenize as get_tokens

from documentor.semantic.models.base import BaseSemanticModel


class SimpleFragment(Fragment):
    """
    Represents a simple fragment of document

    """
    data: str
    tokens: np.ndarray | None
    lemmas: list[str] | None

    def __init__(self, row, *args, **kwargs):
        self.data = row

    def __str__(self, *args, **kwargs):
        """
        Represents a simple fragment of document
        :return: str
        """
        return str(self.data)
