"""Document types for different source formats."""

from .base import Document
from .text import TextDocument
from .word import WordDocument, DocxDocument

__all__ = [
    "Document",
    "TextDocument",
    "WordDocument",
    "DocxDocument", 
]
