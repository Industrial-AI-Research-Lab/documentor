"""LangChain-independent document system."""

from pathlib import Path
from typing import Iterator, Optional

from ..data.structures.fragment.base import Fragment
from ..data.structures.metadata import Metadata
from ..data.structures.structure import DocumentStructure, StructureNode


class Document:
    """
    Document containing a sequence of fragments.
    
    Replaces LangChain Document with independent implementation.
    
    Attributes:
        metadata: Document metadata (path, size, processing method, etc.)
        structure: Optional hierarchical document structure
    """
    
    def __init__(
        self,
        fragments: list[Fragment],
        metadata: Optional[Metadata] = None,
        structure: Optional[DocumentStructure] = None,
    ) -> None:
        """
        Initialize document.
        
        Args:
            fragments: List of document fragments
            metadata: Document metadata
            structure: Hierarchical structure (if available)
        """
        self._fragments = fragments or []
        self.metadata = metadata or Metadata()
        self.structure = structure
    
    def fragments(self) -> list[Fragment]:
        """
        Get list of all document fragments.
        
        Returns:
            list[Fragment]: All fragments in the document
        """
        return self._fragments
    
    def iter_fragments(self) -> Iterator[Fragment]:
        """
        Iterate over fragments without creating list copy.
        
        Yields:
            Fragment: Next document fragment
        """
        for fragment in self._fragments:
            yield fragment
    
    def add_fragment(self, fragment: Fragment) -> None:
        """Add fragment to document."""
        self._fragments.append(fragment)
    
    def create_structure_from_headers(self) -> Optional[DocumentStructure]:
        """
        Create hierarchical structure from headers.
        
        Analyzes HeaderFragments and creates tree structure.
        
        Returns:
            Optional[DocumentStructure]: Created structure or None
        """
        from ..data.structures.fragment.hierarchy import HeaderFragment
        
        # Find all headers and determine levels
        level_pairs = []
        current_level = 0
        
        for fragment in self._fragments:
            if isinstance(fragment, HeaderFragment):
                # Determine header level (logic can be extended)
                if hasattr(fragment, 'level') and fragment.level is not None:
                    level = fragment.level
                else:
                    # Simple style-based heuristic
                    level = current_level
                
                level_pairs.append((level, fragment))
                current_level = level
            else:
                # Regular fragments go one level below last header
                level_pairs.append((current_level + 1, fragment))
        
        if not level_pairs:
            return None
        
        try:
            # TODO: Implement DocumentStructure.from_level_pairs
            # self.structure = DocumentStructure.from_level_pairs(level_pairs)
            # return self.structure
            return None
        except Exception:
            # If structure creation failed, return None
            return None
    
    @classmethod
    def from_path(cls, file_path: Path, fragments: list[Fragment]) -> "Document":
        """
        Create document from file path.
        
        Args:
            file_path: Path to file
            fragments: Document fragments
            
        Returns:
            Document: Created document with metadata
        """
        metadata = Metadata.from_path(file_path)
        return cls(fragments=fragments, metadata=metadata)
    
    def __len__(self) -> int:
        """Number of fragments in document."""
        return len(self._fragments)
    
    def __str__(self) -> str:
        """String representation of document."""
        content_preview = ""
        if self._fragments:
            first_fragments = self._fragments[:3]
            content_preview = " | ".join(str(f.value)[:50] for f in first_fragments)
            if len(self._fragments) > 3:
                content_preview += f" ... (+{len(self._fragments) - 3} more)"
        
        return f"Document(path={self.metadata.file_path}, fragments={len(self._fragments)}, preview='{content_preview}')"
