from typing import Any
from abc import ABC, abstractmethod

from documentor.structuries.type_check import check_str


class FragmentInterface(ABC):
    @property
    @abstractmethod
    def value(self) -> str:
        """
        Get value of the fragment.

        :return: value of the fragment
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

    @abstractmethod
    def params(self) -> dict[str, Any]:
        """
        Get parameters of the fragment.

        :return: parameters of the fragment
        :rtype: dict
        """
        pass


class Fragment(FragmentInterface, ABC):
    """
    Abstract class for fragments of any type. Fragments are structural units of a document.

    Each fragment represents a structural unit of a document,
    for example, a table cell, a log entry, a paragraph of a document with a string value and parameters.
    """
    _value: str

    def __init__(self, value: str) -> None:
        """
        Simple realization of fragment with string value.

        :param value: value of fragment
        :type value: str
        :return: None
        :raises TypeError: if the object is not str
        """
        check_str(value)
        self._value = value

    @property
    def value(self) -> str:
        """
        Get value of the fragment.

        :return: value of the fragment
        :rtype: str
        """
        return self._value

    def __str__(self) -> str:
        """
        String representation of fragment's value.

        :return: value of fragment
        :rtype: str
        """
        return self.value

    def params(self) -> dict[str, Any]:
        """
        Returns an empty dictionary.

        :return: empty dictionary
        :rtype: dict
        """
        return {"value": self.value}
