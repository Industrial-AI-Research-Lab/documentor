from abc import ABC, abstractmethod


class BaseSemanticModel(ABC):
    """
    Abstract class for semantic models interface
    """
    model: any

    def __init__(self, model=None):
        self.model = model

    @abstractmethod
    def load_weights(self, path, *args, **kwargs):
        """
        load weights for model if needed
        :param path:
        :return:
        """
        ...

    @abstractmethod
    def encode(self, X, *args, **kwargs):
        """
        process the data and return it
        :param X: Data for processing
        :type X: np.Array
        :return:
        """
        ...
