import collections
from abc import ABC, abstractmethod

import numpy as np


# Special type for nlp text model
TextModelType = any


class BaseSemanticModel(ABC):
    """
    Abstract class for semantic models interface.
    Text processing models should use this class as parent
    :param model: Some text processing model
    :type model: any
    """
    _model: TextModelType

    def __init__(self, model: TextModelType = None):
        """
        Initialize instance of SemanticModel class
        :param model: The model to be used as a performer or None, if you want load model after
        """
        self._model: TextModelType = model

    def load_weights(self, *args, **kwargs):
        """
        Method for load weights into model
        :param args: some args, must be a path or file or any entity
        :return: None
        """
        ...

    def encode(self, data) -> np.ndarray:
        """
        Base method for encoding
        :param data: Any collections for handling via
        :type data: str or tuple[str]
        :return: numpy array of tokens
        :rtype: np.ndarray
        """
        ...

    def encode_text(self, text: str, *args, **kwargs) -> np.ndarray | tuple[str] | None:
        """
        Method for encoding text that contain several words
        :param text: a long string of words separated by spaces
        :param text: str
        :param args:
        :param kwargs:
        :return: matrix or tuple of processed words
        """
        ...

    def encode_word(self, word: str, *args, **kwargs) -> np.ndarray | str | None:
        """
        Method for encoding a single word
        :param word: a single word
        :type word: str
        :param args:
        :param kwargs:
        :return: matrix of processed word
        """
        ...
