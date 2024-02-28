from abc import ABC, abstractmethod

import numpy as np


class BaseSemanticModel(ABC):
    """
    Abstract class for semantic models interface.
    Text processing models should use this class as parent
    :param model: Some text processing model
    :type model: any
    """
    _model: any

    def __init__(self, model=None):
        self._model = model

    @abstractmethod
    def load_weights(self):
        """
        Method for load weights into model
        :param args: some args, must be a path or file or any entity
        :return: None
        """
        ...

    @abstractmethod
    def encode(self, X) -> np.ndarray:
        """
        base method for encoding
        :param X: Data for processing
        :type X: str or tuple[str]
        :return: numpy array of tokens
        :rtype: np.ndarray
        """
        ...

    @abstractmethod
    def encode_text(self, X: str, *args, **kwargs) -> np.ndarray | tuple[str] | None:
        """
        Method for encoding text that contain several words
        :param X: a long string of words separated by spaces
        :param X: str
        :param args:
        :param kwargs:
        :return: matrix or tuple of processed words
        """
        ...

    @abstractmethod
    def encode_word(self, X: str, *args, **kwargs) -> np.ndarray | str | None:
        """
        Method for encoding a single word
        :param X: a single word
        :type X: str
        :param args:
        :param kwargs:
        :return: matrix of processed word
        """
        ...