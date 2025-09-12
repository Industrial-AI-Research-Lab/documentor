"""Document types for different source formats."""

from .base import Document
from .doc import DocDocument
from .sheet import SheetDocument
from .text import TextDocument

__all__ = [
    "Document",
    "DocDocument", 
    "SheetDocument",
    "TextDocument",
]
