from abc import ABC, abstractmethod

from documentor.structuries.document import Document


class BaseSemanticModel(ABC):
    """
    A base class for semantic model
    """
    @abstractmethod
    def __init__(self, **kwargs):
        ...

    @abstractmethod
    def __call__(self, document: Document, **kwargs):
        ...


