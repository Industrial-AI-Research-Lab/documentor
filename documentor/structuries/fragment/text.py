from dataclasses import dataclass
from typing import Any

from overrides import overrides

from documentor.structuries.fragment.base import Fragment
from structuries.fragment.description import PARAGRAPH


@dataclass
class TextFragment(Fragment):
    """
    Implementation for general text fragments that have only str value.

    Args:
        value (str): Value of the fragment.
    """
    value: str
    description: str = ""


    @overrides
    def __str__(self) -> str:
        return self.value

    @overrides
    def __dict__(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in self.__annotations__.keys()}

@dataclass
class ParagraphFragment(TextFragment):
    """
    Implementation for paragraph text fragments that have only str value.
    """
    description: str = PARAGRAPH
    pass
