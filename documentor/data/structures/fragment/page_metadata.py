"""
Page metadata fragment implementations.

Contains:
- PageHeaderFragment: repeating header information at the top of pages.
- PageFooterFragment: repeating footer information at the bottom of pages.
"""

from dataclasses import dataclass
from typing import Any

from .text import TextFragment


@dataclass
class PageHeaderFragment(TextFragment):
    """
    Implementation for page header fragments containing repeating header information.

    Page headers appear at the top of pages and typically contain section titles,
    chapter names, or other metadata that repeats across multiple pages.

    Attributes:
        value (str): Header text content.
        page_number (str | None): Page number if present in the header.
        section_title (str | None): Section or chapter title if present.
    """

    page_number: str | None = None
    section_title: str | None = None

    @classmethod
    def description(cls) -> str:
        return "Repeating header information at the top of pages"

    def __dict__(self) -> dict[str, Any]:
        """Get parameters of the page header fragment."""
        data = super().__dict__()
        data.update({
            "page_number": self.page_number,
            "section_title": self.section_title,
        })
        return data


@dataclass
class PageFooterFragment(TextFragment):
    """
    Implementation for page footer fragments containing repeating footer information.

    Page footers appear at the bottom of pages and typically contain page numbers,
    publication information, or other metadata that repeats across multiple pages.

    Attributes:
        value (str): Footer text content.
        page_number (str | None): Page number if present in the footer.
        publication_info (str | None): Publication information if present.
    """

    page_number: str | None = None
    publication_info: str | None = None

    @classmethod
    def description(cls) -> str:
        return "Repeating footer information at the bottom of pages"

    def __dict__(self) -> dict[str, Any]:
        """Get parameters of the page footer fragment."""
        data = super().__dict__()
        data.update({
            "page_number": self.page_number,
            "publication_info": self.publication_info,
        })
        return data
