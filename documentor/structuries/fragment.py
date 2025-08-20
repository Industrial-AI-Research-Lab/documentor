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

        Returns:
            str: Value of the fragment.
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """
        Get parameters of the fragment.

        Returns:
            dict[str, Any]: Parameters of the fragment.
        """
        pass

    @classmethod
    @abstractmethod
    def param_types_dict(cls) -> dict[str, type | UnionType]:
        """
        Get types of parameters of the fragment.

        Returns:
            dict[str, type | UnionType]: Types of parameters of the fragment.
        """
        pass


@dataclass
class Fragment(FragmentInterface):
    """
    Simple implementation of FragmentInterface for text fragments that have only value.

    Args:
        value (str): Value of the fragment.
        ground_truth (LabelType | None, optional): Ground truth label of the fragment if it is labeled. Defaults to None.
        label (LabelType | None, optional): Label of the fragment from classification. Defaults to None.
        vector (VectorType | None, optional): Vector representation of the fragment. Defaults to None.
        tokens (list[str] | None, optional): List of tokens of the fragment. Defaults to None.
        token_vectors (list[VectorType] | None, optional): List of vectors of tokens of the fragment. Defaults to None.
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
        # tc.check_simple_type(self.ground_truth, str | int | list | None)
        # tc.check_simple_type(self.label, str | int | list | None)
        # tc.check_simple_type(self.vector, list | None)
        # tc.check_simple_type(self.tokens, list | None)
        # tc.check_simple_type(self.token_vectors, list | None)
        pass

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
