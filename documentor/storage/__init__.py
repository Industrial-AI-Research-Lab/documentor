"""
Module for structured storage of processed documents.

Supports saving documents in JSON format with separate fragment images,
indexing and deduplication.
"""

from .structured_storage import StructuredDocumentStorage
from .document_serializer import DocumentSerializer

__all__ = [
    'StructuredDocumentStorage',
    'DocumentSerializer'
]
