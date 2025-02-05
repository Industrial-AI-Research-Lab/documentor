from typing import Iterator

from langchain_core.documents import Document
from langchain_core.documents.base import Blob

from documentor.loaders.logger import Logger
from documentor.parsers.base import BaseBlobParser
from documentor.parsers.extensions import DocExtension


class TextBlobParser(BaseBlobParser):
    """
    Parser for text blobs.

    Attributes:
        batch_lines (int): The number of lines which is one Document.
            0 value means that whole text blob is one Document.
        _extension (set[DocExtension]): The set of file extensions associated with the parser. Not to be modified.
    """
    batch_lines = 0
    _extension = {DocExtension.txt}

    def __init__(self, batch_lines: int = 0):
        """
        Initialize the TextBlobParser.

        Args:
            batch_lines (int): The number of lines which is one Document.
                0 value means that whole text blob is one Document. Value should be greater than or equal to 0.
            Defaults to 0.
        """
        if not isinstance(batch_lines, int) or batch_lines < 0:
            raise ValueError("batch_lines must be a non-negative integer.")
        self.batch_lines = batch_lines
        self._logs = Logger()

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """
        Lazy parsing of text blobs.

        Args:
            blob (Blob): A Blob object containing the text data.

        Yields:
            Document: A Document object containing the parsed data.
        """
        text = blob.as_string()
        lines = text.splitlines()

        # if batch_lines == 0, then whole text is one Document
        if self.batch_lines == 0:
            # TODO remove code duplication in init Document (three times very similar init)
            yield Document(
                page_content=text.strip(),
                metadata={
                    "file_name": blob.source_path.name if blob.source_path else None,
                    "source": str(blob.source_path) if blob.source_path else None,
                    "file_type": blob.source_path.suffix if blob.source_path else None
                }
            )
        else:
            buffer = []
            for line_number, line in enumerate(lines):
                buffer.append(line)
                # when buffer has enough lines, form Document
                if len(buffer) == self.batch_lines:
                    yield Document(
                        page_content="\n".join(buffer).strip(),
                        metadata={
                            "start_line": line_number - self.batch_lines + 1,
                            "end_line": line_number,
                            "file_name": blob.source_path.name if blob.source_path else None,
                            "source": str(blob.source_path) if blob.source_path else None,
                            "file_type": blob.source_path.suffix if blob.source_path else None
                        }
                    )
                    buffer = []

            # if there are unprocessed lines after the cycle
            if buffer:
                start_line = len(lines) - len(buffer)

                yield Document(
                    page_content="\n".join(buffer).strip(),
                    metadata={
                        "start_line": start_line,
                        "end_line": len(lines) - 1,
                        "file_name": blob.source_path.name if blob.source_path else None,
                        "source": str(blob.source_path) if blob.source_path else None,
                        "file_type": blob.source_path.suffix if blob.source_path else None
                    }
                )
