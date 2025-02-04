import os
from typing import Iterator

from langchain_core.documents.base import Blob
from overrides import overrides
from langchain_core.documents import Document
from documentor.loaders.base import BaseLoader
from pathlib import Path
import zipfile
from documentor.loaders.logger import Logger
from loaders.parsers.text_parser import UnifiedTextBlobParser


class RecursiveLoader(BaseLoader):
    """
    Loader for recursive directory traversal and optional ZIP file processing.
    """

    def __init__(
            self,
            file_path: str | Path,
            extension: list[str] = None, #extension of files to load
            recursive: bool = True,
            zip_loader: bool = False,
            **kwargs
    ):
        """
        Initialize the RecursiveLoader.

        Args:
            file_path (Union[str, Path]): Path to the directory or file.
            extension (list[str], optional): List of file extensions to load. Defaults to all files.
            recursive (bool): Whether to traverse directories recursively. Defaults to True.
            zip_loader (bool): Whether to process ZIP files. Defaults to False.
            log_level (int): Logging level. Defaults to logging.INFO.
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise ValueError(f"Path {self.file_path} does not exist.")

        self.extension = extension if extension else ['*']
        if not isinstance(self.extension, list) or not all(isinstance(ext, str) for ext in self.extension):
            raise ValueError("Extension must be a list of strings.")

        self.recursive = recursive
        self.zip_loader = zip_loader

        # Initialize logs
        self._logs = Logger()


    @staticmethod
    def _create_document(content: str, line_number: int, file_name: str, source: str, file_type: str) -> Document:
        """
        Helper method to create a Document object.

        Args:
            content (str): Content of the document.
            line_number (int): Line number in the file.
            file_name (str): Name of the file.
            source (str): Source path or identifier.
            file_type (str): Type of the file.

        Returns:
            Document: The created document.
        """
        return Document(
            page_content=content,
            metadata={
                "line_number": line_number,
                "file_name": file_name,
                "source": source,
                "file_type": file_type
            }
        )

    def _is_valid_extension(self, path: Path) -> bool:
        """
        Check if the file has a valid extension.

        Args:
            path (Path): Path to the file.

        Returns:
            bool: True if the file has a valid extension, False otherwise.
        """
        return self.extension == ['*'] or path.suffix.lower().lstrip('.') in [ext.lower() for ext in self.extension]

    def _process_file(self, path: Path) -> Iterator[Document]:
        """
        Process a single file and yield Document objects line by line.

        Args:
            path (Path): Path to the file.

        Yields:
            Iterator[Document]: Document objects.
        """
        self._logs.add_info(f"Reading file: {path}")
        # TODO вынести объявление все парсеров используемых в лоадере в init. То есть мы объявляем лоадер и настраиваем
        #  его при создании вместе с расшиерниями и парсерами
        parser = UnifiedTextBlobParser()
        try:


            blob = Blob.from_path(path)
            documents = parser.parse(blob)
            for document in documents:
                yield document
        except ValueError as e:
            self._logs.add_warning(str(e))
        except RuntimeError as e:
            self._logs.add_error(str(e))


    def _process_zip(self, path: Path) -> Iterator[Document]:
        """
        Process a ZIP file and yield Document objects for each line in each file.

        Args:
            path (Path): Path to the ZIP file.

        Yields:
            Iterator[Document]: Document objects.
        """
        self._logs.add_info(f"Processing ZIP archive: {path}")
        try:
            with zipfile.ZipFile(path, 'r') as zip_ref:

                for name in zip_ref.namelist():
                    # We assume all files inside the ZIP are valid for processing
                    try:
                        with zip_ref.open(name) as f:
                            content = f.read().decode('utf-8')
                            for line_number, line in enumerate(content.splitlines()):
                                yield self._create_document(
                                    content=line.strip(),
                                    line_number=line_number,
                                    file_name=name,
                                    source=f"{path}!{name}",
                                    file_type="zip-content"
                                )
                    except UnicodeDecodeError:
                        self._logs.add_warning(f"Cannot decode file {name} in ZIP archive {path}")
                    except Exception as e:
                        self._logs.add_error(f"Error reading file {name} in ZIP archive {path}: {str(e)}")

        except Exception as e:
            self._logs.add_error(f"Error processing ZIP file {path}: {str(e)}")


    @overrides
    def lazy_load(self) -> Iterator[Document]:
        """
        Lazy loading of documents line by line.

        Yields:
            Iterator[Document]: Document objects.
        """
        pattern = '**/*' if self.recursive else '*'

        for path in self.file_path.glob(pattern):
            if path.is_file() and (
                    self._is_valid_extension(path) or (self.zip_loader and path.suffix.lower() == '.zip')):
                documents = (
                    self._process_zip(
                        path) if self.zip_loader and path.suffix.lower() == '.zip' else self._process_file(path)
                )

                for doc in documents:
                    yield doc
