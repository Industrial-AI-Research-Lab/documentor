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

    Attributes:
        value (str): Header text.
        font_size (int | None): Optional font size of the header.
        level (int | None): Optional hierarchical level (e.g., 1 for H1).
        description (str): Fragment type description for LLMs.
    """
    font_size: int | None = None
    level: int | None = None
    description: str = HEADER


class TitleFragment(HeaderFragment):
    """
    The title of the document.

    Attributes:
        value (str): Title text.
        font_size (int | None): Optional font size of the title.
        level (int | None): Optional hierarchical level.
        description (str): Fragment type description for LLMs.
    """
    description: str = TITLE


class ColumnHeaderFragment(HeaderFragment):
    """
    Column header (e.g., column number) text fragment with only a str value.

    Attributes:
        value (str): Column header text.
        font_size (int | None): Optional font size of the header.
        level (int | None): Optional hierarchical level.
        description (str): Fragment type description for LLMs.
    """
    description: str = COLUMN
