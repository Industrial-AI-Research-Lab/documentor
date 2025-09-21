"""
Word document types for DOC/DOCX files.

Contains document classes specific to Microsoft Word formats:
- WordDocument: Base class for Word documents
- DocxDocument: DOCX format documents  
- DocDocument: DOC format documents
"""

from typing import Optional, Dict, Any, List
from .base import Document
from ..metadata import Metadata
from ..fragment import Fragment


class WordDocument(Document):
    """
    Base document type for Microsoft Word documents.
    
    Contains Word-specific metadata and properties common to both
    DOC and DOCX formats.
    
    Attributes:
        pages_count: Total number of pages
        word_count: Total word count
        character_count: Total character count  
        document_properties: Word document properties
        sections_count: Number of document sections
        has_headers_footers: Whether document has headers/footers
        has_footnotes: Whether document has footnotes
        has_comments: Whether document has comments
        has_track_changes: Whether document has tracked changes
    """
    
    def __init__(
        self,
        fragments: List[Fragment],
        pages_count: int = 1,
        word_count: int = 0,
        character_count: int = 0,
        document_properties: Optional[Dict[str, Any]] = None,
        sections_count: int = 1,
        has_headers_footers: bool = False,
        has_footnotes: bool = False,
        has_comments: bool = False,
        has_track_changes: bool = False,
        **kwargs
    ):
        super().__init__(fragments=fragments, **kwargs)
        self.pages_count = pages_count
        self.word_count = word_count
        self.character_count = character_count
        self.document_properties = document_properties or {}
        self.sections_count = sections_count
        self.has_headers_footers = has_headers_footers
        self.has_footnotes = has_footnotes
        self.has_comments = has_comments
        self.has_track_changes = has_track_changes
    
    def get_document_info(self) -> Dict[str, Any]:
        """Get comprehensive document information."""
        return {
            "pages_count": self.pages_count,
            "word_count": self.word_count,
            "character_count": self.character_count,
            "sections_count": self.sections_count,
            "has_headers_footers": self.has_headers_footers,
            "has_footnotes": self.has_footnotes,
            "has_comments": self.has_comments,
            "has_track_changes": self.has_track_changes,
            "fragments_count": len(self.fragments()),
            "document_properties": self.document_properties
        }


class DocxDocument(WordDocument):
    """
    Document type for DOCX format files.
    
    DOCX files are XML-based and provide rich structure information
    including styles, themes, and embedded objects.
    
    Attributes:
        xml_structure: Raw XML structure information
        styles: Document styles information
        themes: Document themes
        embedded_objects: List of embedded objects (images, charts, etc.)
    """
    
    def __init__(
        self,
        fragments: List[Fragment],
        xml_structure: Optional[Dict[str, Any]] = None,
        styles: Optional[Dict[str, Any]] = None,
        themes: Optional[Dict[str, Any]] = None,
        embedded_objects: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ):
        super().__init__(fragments=fragments, **kwargs)
        self.xml_structure = xml_structure or {}
        self.styles = styles or {}
        self.themes = themes or {}
        self.embedded_objects = embedded_objects or []
    
    def get_format_info(self) -> Dict[str, Any]:
        """Get DOCX-specific format information."""
        return {
            **self.get_document_info(),
            "format": "DOCX",
            "is_xml_based": True,
            "styles_count": len(self.styles),
            "themes_count": len(self.themes),
            "embedded_objects_count": len(self.embedded_objects),
            "has_xml_structure": bool(self.xml_structure)
        }


class DocDocument(WordDocument):
    """
    Document type for DOC format files.
    
    DOC files are binary format with limited structure extraction
    capabilities compared to DOCX.
    
    Attributes:
        conversion_method: Method used for conversion (e.g., "docx2txt", "libreoffice")
        conversion_quality: Quality assessment of conversion
        original_encoding: Original file encoding if detected
    """
    
    def __init__(
        self,
        fragments: List[Fragment],
        conversion_method: str = "docx2txt",
        conversion_quality: str = "unknown",
        original_encoding: Optional[str] = None,
        **kwargs
    ):
        super().__init__(fragments=fragments, **kwargs)
        self.conversion_method = conversion_method
        self.conversion_quality = conversion_quality
        self.original_encoding = original_encoding
    
    def get_format_info(self) -> Dict[str, Any]:
        """Get DOC-specific format information."""
        return {
            **self.get_document_info(),
            "format": "DOC",
            "is_xml_based": False,
            "conversion_method": self.conversion_method,
            "conversion_quality": self.conversion_quality,
            "original_encoding": self.original_encoding
        }
