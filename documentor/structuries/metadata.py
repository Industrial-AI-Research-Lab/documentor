from typing import Any, Optional

from langchain_core.documents.base import Blob


class Metadata:
    name: Optional[str] = None
    extension: Optional[str] = None
    source: Optional[Blob] = None
    params: dict[str, Any] = {}

    def __init__(
            self,
            name: Optional[str] = None,
            extension: Optional[str] = None,
            source: Optional[Blob] = None,
            **kwargs,
    ):
        self.name = name
        self.extension = extension
        self.source = source
        self.params = kwargs


def to_document_metadata(
        meta: Metadata,
        *,
        extension_key: str = "extension",
        name_key: str = "file_name",
        include_source: bool = True,
        stringify_source_path: bool = True,
) -> dict[str, Any]:
    """
    Convert a Metadata instance to a dict suitable for langchain Document.metadata.

    Args:
        meta: Metadata instance with name/extension/source and arbitrary params.
        extension_key: Key name to use for the file extension field in the dict.
                        For backward compatibility, TextBlobParser expects "file_type",
                        while ExcelBlobParser expects "extension".
        name_key: Key name to use for the file name field (usually "file_name").
        include_source: Whether to include a "source" field in the result.
        stringify_source_path: If True and source has a path, convert it to str.

    Returns:
        dict[str, Any]: Flattened metadata for Document.metadata.
    """
    result: dict[str, Any] = {}
    # File name and extension under requested keys
    if name_key:
        result[name_key] = meta.name
    if extension_key:
        result[extension_key] = meta.extension

    # Source: prefer Blob.path string for portability in tests/consumers
    if include_source:
        if meta.source is not None and hasattr(meta.source, "path") and meta.source.path is not None:
            result["source"] = str(meta.source.path) if stringify_source_path else meta.source.path
        else:
            result["source"] = None

    # Merge arbitrary params (e.g., line_number, sheet_name)
    if meta.params:
        result.update(meta.params)

    return result
