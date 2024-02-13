from abc import ABC, abstractmethod
from dataclasses import dataclass


class Fragment(ABC):
    """
    Abstract class for fragments of document.

    Each fragment represents a structural unit of a document,
    for example, a table cell, a log entry, a paragraph of a document with a string value and parameters.
    """
    @property
    @abstractmethod
    def value(self) -> str:
        """
        Value of fragment.

        :return: the value
        :rtype: str
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        String representation of fragment's value.
        :return: value of fragment
        :rtype: str
        """
        pass
