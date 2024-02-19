from abc import ABC, abstractmethod

import numpy as np


class BaseSemanticModel(ABC):
    """
    Abstract class for semantic models interface.
    Text processing models should use this class as parent
    :param model: Some text processing model
    :type model: any
    """
    model: any

    def __init__(self, model=None):
        self.model = model

    @abstractmethod
    def load_weights(self, *args, **kwargs):
        """
        Method for load weights into model
        :param args: some args, must be a path or file or any entity
        :return: None
        """
        ...

    @abstractmethod
    def encode(self, X, *args, **kwargs) -> np.ndarray:
        """
        process the data and return it
        :param X: Data for processing
        :type X: any collection words or one words
        :return: numpy array of tokens
        :rtype: np.ndarray
        """
        ...
