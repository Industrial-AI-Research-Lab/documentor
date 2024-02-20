from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from types import UnionType
from typing import Any

from overrides import overrides

from documentor.structuries.type_check import TypeChecker as tc


class FragmentInterface(ABC):
    """
    Interface for fragments of any type.

    Each fragment represents a structural unit of a document.
    Examples of fragments:
    - a table cell
    - a log entry
    - a sentence or paragraph of a document with a string value and parameters.
    """

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

    @classmethod
    @abstractmethod
    def param_types_dict(cls) -> dict[str, type | UnionType]:
        """
        Get parameters types of the fragment.

        :return: parameters types of the fragment
        :rtype: dict
        """
        pass


LabelType = str | int


class ParamEnum(Enum):
    """
    Enum for Document columns.
    """
    VALUE = ("value", str, True)
    GROUND_TRUTH = ("ground_truth", LabelType, False)
    LABEL = ("label", LabelType, False)
    VECTOR = ("vector", Any, False)
    TOKENS = ("tokens", list[str], False)
    TOKEN_VECTORS = ("token_vectors", list[Any], False)


@dataclass
class Fragment(FragmentInterface):
    """
    Abstract class for fragments of any type. Fragments are structural units of a document.

    Each fragment represents a structural unit of a document,
    for example, a table cell, a log entry, a paragraph of a document with a string value and parameters.
    """
    value: str
    ground_truth: str | int | None
    label: str | int | None
    vector: Any | None
    tokens: list[str] | None
    token_vectors: list[Any] | None

    def __init__(self, value: str) -> None:
        """
        Simple realization of fragment with string value.

        :param value: value of fragment
        :type value: str
        :return: None
        :raises TypeError: if the object is not str
        """
        tc.check_str(value)
        self._value = value

    @overrides
    def __str__(self) -> str:
        return self.value

    @overrides
    def params(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in self.__annotations__.keys()}
