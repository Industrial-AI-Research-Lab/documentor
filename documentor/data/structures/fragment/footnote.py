"""
Footnote fragment implementation.

Contains:
- FootnoteFragment: footnotes providing supplementary information or citations.
"""

from dataclasses import dataclass
from typing import Any

from .text import TextFragment


@dataclass
class FootnoteFragment(TextFragment):
    """
    Implementation for footnote fragments providing supplementary information.

    Footnotes are additional notes, citations, or explanations that appear
    at the bottom of pages, referenced by markers in the main text.

    Attributes:
        value (str): Footnote text content.
        footnote_number (str | None): Number or identifier of the footnote.
        reference_marker (str | None): Marker used in the main text to reference this footnote.
    """

    footnote_number: str | None = None
    reference_marker: str | None = None

    @classmethod
    def description(cls) -> str:
        return "Supplementary information or citations at the bottom of pages"

    def __dict__(self) -> dict[str, Any]:
        """Get parameters of the footnote fragment."""
        data = super().__dict__()
        data.update({
            "footnote_number": self.footnote_number,
            "reference_marker": self.reference_marker,
        })
        return data
