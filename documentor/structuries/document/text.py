from structuries.document.base import Document


class TextDocument(Document):
    """
    Document type for plain text sources.

    Attributes:
        lines_count: Number of text lines in the source (if known).
    """
    lines_count: int
