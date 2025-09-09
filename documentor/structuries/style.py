"""Style structures for fragments."""
from dataclasses import dataclass


@dataclass
class BlockStyle:
    """Block-level styling information for a fragment."""
    font_family: str | None = None
    font_size: float | None = None
    font_weight: str | None = None
    alignment: str | None = None
    color: str | None = None
    line_height: float | None = None


@dataclass
class InlineStyle:
    """Placeholder for future inline-level styling."""
    bold: bool | None = None
    italic: bool | None = None
    underline: bool | None = None
    color: str | None = None
