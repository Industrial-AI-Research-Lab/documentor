from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import UnionType
from typing import Any

from overrides import overrides

from documentor.structuries.custom_types import LabelType, VectorType
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
    value: str

    @abstractmethod
    def __str__(self) -> str:
        """
        String representation of fragment's value.

        :return: value of fragment
        :rtype: str
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
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
        Get types of parameters of the fragment.

        :return: types of parameters of the fragment
        :rtype: dict[str, type | UnionType]
        """
        pass


@dataclass
class Fragment(FragmentInterface):
    """
    Class for simple realization of FragmentInterface for text fragments, which have only value.

    :param value: value of the fragment
    :type value: str
    :param ground_truth: ground truth label of the fragment, if it is labeled
    :type ground_truth: Optional[LabelType]
    :param label: label of the fragment from classification
    :type label: Optional[LabelType]
    :param vector: vector representation of the fragment
    :type vector: Optional[VectorType]
    :param tokens: list of tokens of the fragment
    :type tokens: Optional[list[str]]
    :param token_vectors: list of vectors of tokens of the fragment
    :type token_vectors: Optional[list[VectorType]]
    """
    value: str
    ground_truth: LabelType | None = None
    label: LabelType | None = None
    vector: VectorType | None = None
    tokens: list[str] | None = None
    token_vectors: list[VectorType] | None = None

    def __post_init__(self) -> None:
        # TODO: add type checking for complex types
        tc.check_str(self.value)
        tc.check_simple_type(self.ground_truth, str | int | list | None)
        tc.check_simple_type(self.label, str | int | list | None)
        tc.check_simple_type(self.vector, list | None)
        tc.check_simple_type(self.tokens, list | None)
        tc.check_simple_type(self.token_vectors, list | None)

    @overrides
    def __str__(self) -> str:
        return self.value

    @overrides
    def to_dict(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in self.__annotations__.keys()}

    @classmethod
    @overrides
    def param_types_dict(cls) -> dict[str, type | UnionType]:
        return {param: param_type for param, param_type in cls.__annotations__.items()}
