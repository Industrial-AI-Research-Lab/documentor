"""Core base classes for document system."""

from .document import Document
from .interfaces import BaseLoader, BaseParser
from .logging import get_logger

__all__ = [
    "Document",
    "BaseLoader", 
    "BaseParser",
    "get_logger",
]
