"""Structuries module for document processing and structure management."""

# Custom types
from .custom_types import LabelType, VectorType

# Column definitions
from .columns import ColumnType

# Metadata handling
from .metadata import Metadata, to_document_metadata

# Style definitions
from .style import BlockStyle, InlineStyle

# Structure management
from .structure import StructureNode, DocumentStructure

# Document types
from .document import Document, DocDocument, SheetDocument, TextDocument

# Classifier interfaces
from .classifier import ClassifierModel, FragmentClassifier

__all__ = [
    # Custom types
    "LabelType",
    "VectorType",
    
    # Column definitions
    "ColumnType",
    
    # Metadata
    "Metadata",
    "to_document_metadata",
    
    # Styles
    "BlockStyle", 
    "InlineStyle",
    
    # Structure
    "StructureNode",
    "DocumentStructure",
    
    # Document types
    "Document",
    "DocDocument",
    "SheetDocument", 
    "TextDocument",
    
    # Classifiers
    "ClassifierModel",
    "FragmentClassifier",
]
