from abc import ABC, abstractmethod


class BaseEstimator(ABC):
    """
    Base class for integrate extended library models
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        ...

    @abstractmethod
    def __call__(self, *args, **kwargs):
        ...
