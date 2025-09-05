from typing import Iterator

try:  # pragma: no cover - optional langchain dependency
    from langchain_core.documents import Document as LCDocument
except Exception:  # pragma: no cover
    class LCDocument:  # type: ignore[override]
        def __init__(self, page_content: str = "", metadata: dict | None = None) -> None:
            self.page_content = page_content
            self.metadata = metadata or {}

import pandas as pd

from structuries.fragment import Fragment
from structuries.metadata import Metadata
from structuries.structure import DocumentStructure


class Document(LCDocument):
    """
    Base interface for documents that contain a sequence of fragments.

    A document is a container over parsed fragments (text, tables, images, etc.)
    and may optionally hold a higher-level structure description.

    Attributes:
        structure: Optional document structure (e.g., a tree of sections) associated with this document.
    """
    # Instance attributes are initialized in __init__ to avoid shared mutable defaults.
    _fragments: list[Fragment]
    structure: DocumentStructure | None
    metadata: Metadata

    def __init__(
        self,
        fragments: list[Fragment],
        structure: DocumentStructure | None = None,
        metadata: Metadata | None = None,
    ) -> None:
        """Initialize a Document."""
        if metadata is None:
            metadata = Metadata()
        text = "\n".join(str(fragment) for fragment in fragments)
        super().__init__(page_content=text, metadata=dict(metadata.__dict__))
        self._fragments = fragments
        self.structure = structure
        self.metadata = metadata

    def fragments(self) -> list[Fragment]:
        """
        Get the list of document fragments.

        Note:
            If speed is important, prefer using iter_fragments().

        Returns:
            list[Fragment]: List of fragments in the document.
        """
        return self._fragments

    def iter_fragments(self) -> Iterator[Fragment]:
        """
        Iterate over fragments one by one without creating an intermediate list copy.

        Yields:
            Fragment: Next fragment from the document.
        """
        for fragment in self._fragments:
            yield fragment
