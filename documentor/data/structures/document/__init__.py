"""Document types for different source formats."""

from .base import Document
# from .doc import DocDocument  # Removed
# from .sheet import SheetDocument  # Removed
from .text import TextDocument

__all__ = [
    "Document",
    "TextDocument",
]
