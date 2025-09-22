"""Document loader system without LangChain dependencies."""

from .recursive_loader import RecursiveDocumentLoader
from .base import FileWatcher

__all__ = [
    "RecursiveDocumentLoader",
    "FileWatcher",
]
