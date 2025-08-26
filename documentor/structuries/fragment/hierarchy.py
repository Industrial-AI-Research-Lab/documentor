"""
Hierarchy-related fragments: titles and headers.

Contains:
- HeaderFragment: generic header with optional font_size and level.
- TitleFragment: the document title.
- ColumnHeaderFragment: column header/numbering labels.
"""
from dataclasses import dataclass

from .text import TextFragment
from .description import TITLE, COLUMN, HEADER


@dataclass
class HeaderFragment(TextFragment):
    """
    Header text fragments with a str value and header metadata.
    """
    font_size: int | None = None
    level: int | None = None
    description: str = HEADER


class TitleFragment(HeaderFragment):
    """
    The title of the document.
    """
    description: str = TITLE


class ColumnHeaderFragment(HeaderFragment):
    """
    Column header (e.g., column number) text fragment with only a str value.
    """
    description: str = COLUMN
