"""
Text fragments.

Contains:
- TextFragment: plain text fragment base for string content.
- ParagraphFragment: specific paragraph text with PARAGRAPH description.
"""
from dataclasses import dataclass
from typing import Any

try:
    from overrides import overrides
except Exception:
    # Fallback no-op decorator if `overrides` is not installed
    def overrides(method=None, *args, **kwargs):
        if callable(method):
            return method
        def decorator(func):
            return func
        return decorator

from .base import Fragment
from .description import PARAGRAPH


@dataclass
class TextFragment(Fragment):
    """
    Implementation for general text fragments that have only str value.

    Attributes:
        value (str): Value of the fragment.
    """
    value: str

    @classmethod
    def description(cls) -> str:
        return ""

    @overrides
    def __str__(self) -> str:
        return self.value

    @overrides
    def __dict__(self) -> dict[str, Any]:
        return super().__dict__()

class ParagraphFragment(TextFragment):
    """
    Implementation for paragraph text fragments that have only str value.

    Attributes:
        value (str): Text of the paragraph.
    """
    @classmethod
    def description(cls) -> str:
        return PARAGRAPH
