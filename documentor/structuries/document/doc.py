from structuries.document.base import Document


class DocDocument(Document):
    """
    Document type representing multi-page documents (e.g., PDF, DOCX).

    Attributes:
        pages_count: Total number of pages in the source document.
    """
    pages_count: int
