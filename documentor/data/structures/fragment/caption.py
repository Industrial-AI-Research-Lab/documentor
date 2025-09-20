"""
Caption fragment implementation.

Contains:
- CaptionFragment: captions for figures, tables, and formulas.
"""

from dataclasses import dataclass
from typing import Any

from .text import TextFragment


@dataclass
class CaptionFragment(TextFragment):
    """
    Implementation for caption fragments that describe visual elements.

    Captions are short descriptive texts accompanying figures, tables, or formulas.
    They provide context and explanation for visual content in documents.

    Attributes:
        value (str): Caption text content.
        caption_type (str | None): Type of caption - 'figure', 'table', 'formula'.
        target_id (str | None): ID of the associated visual element.
    """

    caption_type: str | None = None
    target_id: str | None = None

    @classmethod
    def description(cls) -> str:
        return "Short descriptive text accompanying figures, tables, or formulas"

    def __dict__(self) -> dict[str, Any]:
        """Get parameters of the caption fragment."""
        data = super().__dict__()
        data.update({
            "caption_type": self.caption_type,
            "target_id": self.target_id,
        })
        return data
