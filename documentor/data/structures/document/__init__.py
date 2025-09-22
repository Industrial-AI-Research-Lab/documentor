"""Document types for different source formats."""

from .base import Document
from .doc import DocDocument
from .text import TextDocument
from .word import WordDocument, DocxDocument, DocDocument as WordDocDocument

__all__ = [
    "Document",
    "DocDocument", 
    "TextDocument",
    "WordDocument",
    "DocxDocument", 
    "WordDocDocument",
]
