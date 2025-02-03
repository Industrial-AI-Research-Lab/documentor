from documentor.loaders.parsers.base import BaseBlobParser, BaseParserType
from langchain_core.documents import Document
from pathlib import Path

from langchain_core.documents.base import Blob
from overrides import overrides
from typing import Iterator

from loaders.parsers.extensions import DocExtension


class UnifiedTextType(BaseParserType):
    """
    UnifiedTextType - Class for text file extensions.
    """

    @classmethod
    def get_extensions(cls) -> set[DocExtension]:
        return {DocExtension.txt}

    @overrides(BaseParserType)
    def is_in(self, extension: str | DocExtension) -> bool:
        return True


class UnifiedTextBlobParser(BaseBlobParser):
    """
    Parser for text blobs.
    """
    _extension = UnifiedTextType()

    def __init__(self, encoding: str = 'utf-8', batch_lines: int = 0):
        """
        Initialize the TextBlobParser.

        Args:
            encoding (str): The encoding to use when reading the text blob. Defaults to 'utf-8'.
            batch_lines (int): The number of lines which is one Document.
                0 value means that whole text blob is one Document. Value should be greater than 0. Defaults to 0.
        """
        self.encoding = encoding
        if not isinstance(batch_lines, int) or batch_lines < 0:
            raise ValueError("batch_lines must be a non-negative integer.")
        self.batch_lines = batch_lines

    @classmethod
    @overrides(BaseBlobParser)
    def get_type(cls):
        return cls._extension

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """
        Lazy parsing of text blobs.

        Args:
            blob (Blob): A Blob object containing the text data.

        Yields:
            Document: A Document object containing the parsed data.
        """
        # TODO rewrite this method to use batch_lines and blob object
        path = Path(file_path)
        try:
            with open(path, 'r', encoding=self,) as f:
                for line_number, line in enumerate(f):
                    yield Document(
                        page_content=line.strip(),
                        metadata={
                            "line_number": line_number,
                            "file_name": path.name,
                            "source": str(path),
                            "file_type": path.suffix
                        }
                    )
        except UnicodeDecodeError:
            raise ValueError(f"Cannot decode file {path}")
        except Exception as e:
            raise RuntimeError(f"Error reading file {path}: {str(e)}")

    @property
    @overrides
    def logs(self) -> dict[str, list[str]]:
        """
        Returns the logs collected during processing.

        Returns:
            dict[str, list[str]]: A dictionary containing lists of log messages for 'info', 'warning', and 'error'.
        """
        return {}
