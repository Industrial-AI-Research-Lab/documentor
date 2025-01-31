from loaders.parsers.base import BaseParser
from langchain_core.documents import Document
from pathlib import Path
from overrides import overrides
from typing import Iterator

class Parser(BaseParser):
    """
    Parser - A parser that can parse a file and return a list of Document objects.
    """
    def __init__(self, 
                 file_path: str|Path, 
                 **kwargs):
        """
        Initializes the Parser.

        Args:
            file_path (str | Path): The path to the file to be parsed.
            **kwargs: Additional keyword arguments for specific parser implementations.
        """
        super().__init__(file_path, **kwargs)
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise ValueError(f"Path {self.file_path} does not exist.")

    @overrides
    def parse(self, file_path: str|Path, **kwargs) -> Iterator[Document]:
        """
        Parses the file at the given path and returns an iterator of Document objects.

        Args:
            file_path (str | Path): The path to the file to be parsed.
            **kwargs: Additional keyword arguments for specific parser implementations.

        Yields:
            Document: A Document object containing the parsed data.
        """
        path = Path(file_path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
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

