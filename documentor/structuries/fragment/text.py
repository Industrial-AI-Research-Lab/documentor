from dataclasses import dataclass
from typing import Any

from overrides import overrides

from documentor.structuries.fragment.base import FragmentInterface


@dataclass
class TextFragment(FragmentInterface):
    """
    Implementation for general text fragments that have only str value.

    Args:
        value (str): Value of the fragment.
    """
    value: str


    @overrides
    def __str__(self) -> str:
        return self.value

    @overrides
    def __dict__(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in self.__annotations__.keys()}

@dataclass
class HeaderFragment(TextFragment):
    """
    Implementation for header text fragments that have only str value.
    """
    font_size: int | None = None
    level: int | None = None

class TitleFragment(HeaderFragment):
    """
    Implementation for the title of the document.
    """
    pass


class ColumnHeaderFragment(HeaderFragment):
    """
    Implementation for column header (column number) text fragments that have only str value.
    """
    pass

class ListingFragment(TextFragment):
    """
    Implementation for listing text fragments that have only str value.
    """
    pass

class ParagraphFragment(TextFragment):
    """
    Implementation for paragraph text fragments that have only str value.
    """
    pass
