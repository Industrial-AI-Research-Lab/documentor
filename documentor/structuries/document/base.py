from typing import Iterator

import pandas as pd

from structuries.fragment import Fragment
from structuries.structure import DocumentStructure


class Document:
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

    def __init__(self, fragments: list[Fragment], structure: DocumentStructure | None = None):
        """
        Initialize a Document.

        Args:
            fragments: The list of fragments contained in the document.
            structure: Optional structural representation of the document.
        """
        self._fragments = fragments
        self.structure = structure

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

    def to_df(self) -> pd.DataFrame:
        """
        Convert the document fragments to a pandas DataFrame.

        Each fragment contributes a single row created from its __dict__() representation.

        Returns:
            pd.DataFrame: DataFrame containing one row per fragment.
        """
        data = [f.__dict__() for f in self._fragments]
        return pd.DataFrame(data)
