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


@dataclass
class LayoutStyle(BlockStyle):
    """Layout-specific styling information for fragments.
    
    Extends BlockStyle with layout-specific attributes for better
    understanding of document structure and positioning.
    
    Attributes:
        position: Text alignment within the block.
        column: Column number in multi-column layouts.
        page_region: Region of the page (header, body, footer).
        is_floating: Whether the element floats around other content.
        wraps_around: Whether text wraps around this element.
        spans_columns: Whether the element spans multiple columns.
        hierarchy_level: Hierarchical level within the document structure.
    """
    position: str | None = None        # 'left', 'center', 'right', 'justify'
    column: int | None = None          # Column number
    page_region: str | None = None     # 'header', 'body', 'footer'
    is_floating: bool = False          # Floating element
    wraps_around: bool = False         # Text wraps around
    spans_columns: bool = False        # Spans multiple columns
    hierarchy_level: int = 0           # Hierarchical level