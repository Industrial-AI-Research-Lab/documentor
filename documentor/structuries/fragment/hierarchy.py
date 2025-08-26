from dataclasses import dataclass

from structuries.fragment import TextFragment
from structuries.fragment.description import TITLE, COLUMN


@dataclass
class HeaderFragment(TextFragment):
    """
    Implementation for header text fragments that have only str value.
    """
    font_size: int | None = None
    level: int | None = None
    description: str = HEADER


class TitleFragment(HeaderFragment):
    """
    Implementation for the title of the document.
    """
    description: str = TITLE


class ColumnHeaderFragment(HeaderFragment):
    """
    Implementation for column header (column number) text fragments that have only str value.
    """
    description: str = COLUMN
