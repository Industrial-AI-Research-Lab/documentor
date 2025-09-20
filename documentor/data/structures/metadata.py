from pathlib import Path
from typing import Any, Optional


class Metadata:
    """
    Document metadata without LangChain dependencies.
    
    Contains all necessary information about file and processing method.
    """
    
    def __init__(
            self,
            name: Optional[str] = None,
            extension: Optional[str] = None,
            file_path: Optional[str] = None,
            file_size: Optional[int] = None,
            processing_method: Optional[str] = None,
            **kwargs,
    ):
        """
        Initialize metadata.
        
        Args:
            name: File name
            extension: File extension
            file_path: Full path to file
            file_size: File size in bytes
            processing_method: Processing method ('text_extraction', 'ocr', 'direct')
            **kwargs: Additional parameters
        """
        self.name = name
        self.extension = extension
        self.file_path = file_path
        self.file_size = file_size
        self.processing_method = processing_method
        self.params = kwargs

    @classmethod
    def from_path(cls, path: Path, **kwargs) -> "Metadata":
        """Create metadata from file path."""
        if path.exists():
            file_size = path.stat().st_size
        else:
            file_size = None
            
        return cls(
            name=path.name,
            extension=path.suffix.lower(),
            file_path=str(path),
            file_size=file_size,
            **kwargs
        )


def to_document_metadata(
        meta: Metadata,
        *,
        extension_key: str = "extension",
        name_key: str = "file_name",
        include_path: bool = True,
) -> dict[str, Any]:
    """
    Convert metadata to dictionary for compatibility.

    Args:
        meta: Metadata instance with file information
        extension_key: Key for file extension
        name_key: Key for file name
        include_path: Whether to include file path

    Returns:
        dict[str, Any]: Flat metadata dictionary
    """
    result: dict[str, Any] = {}
    
    # File name and extension
    if name_key:
        result[name_key] = meta.name
    if extension_key:
        result[extension_key] = meta.extension

    # File path
    if include_path:
        result["source"] = meta.file_path

    # Additional information
    result["file_size"] = meta.file_size
    result["processing_method"] = meta.processing_method

    # Additional parameters
    if meta.params:
        result.update(meta.params)

    return result
