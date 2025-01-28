from typing import Union, Iterator, List
from overrides import overrides
from langchain_core.documents import Document
from loaders.base import BaseLoader
from pathlib import Path
import zipfile
import logging


class RecursiveLoader(BaseLoader):
    """
    Loader for recursive directory traversal and optional ZIP file processing.
    """

    def __init__(self, 
                 file_path: Union[str, Path], 
                 extension: List[str] = None, 
                 recursive: bool = True, 
                 zip_loader: bool = False, 
                 encoding: str = 'utf-8',
                 **kwargs):
        """
        Initialize the RecursiveLoader.

        Args:
            file_path (Union[str, Path]): Path to the directory or file.
            extension (List[str], optional): List of file extensions to load. Defaults to all files.
            recursive (bool): Whether to traverse directories recursively. Defaults to True.
            zip_loader (bool): Whether to process ZIP files. Defaults to False.
            encoding (str): Encoding to use for reading files. Defaults to 'utf-8'.
        """
        self.file_path = Path(file_path)
        self.extension = extension if extension else ['*']
        self.recursive = recursive
        self.zip_loader = zip_loader
        self.encoding = encoding

        # Set up logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def _create_document(self, content: str, line_number: int, file_name: str, source: str, file_type: str) -> Document:
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

    def _process_file(self, path: Path) -> Iterator[Document]:
        """
        Process a single file and yield Document objects line by line.

        Args:
            path (Path): Path to the file.

        Yields:
            Iterator[Document]: Document objects.
        """
        self.logger.info(f"Reading file: {path}")
        try:
            with open(path, 'r', encoding=self.encoding) as f:
                for line_number, line in enumerate(f):
                    yield self._create_document(
                        content=line.strip(),
                        line_number=line_number,
                        file_name=path.name,
                        source=str(path),
                        file_type=path.suffix
                    )
        except UnicodeDecodeError:
            self.logger.warning(f"Cannot decode file {path} with encoding {self.encoding}")
        except Exception as e:
            self.logger.error(f"Error reading file {path}: {str(e)}")

    def _process_zip(self, path: Path) -> Iterator[Document]:
        """
        Process a ZIP file and yield Document objects for each line in each file.

        Args:
            path (Path): Path to the ZIP file.

        Yields:
            Iterator[Document]: Document objects.
        """
        self.logger.info(f"Processing ZIP archive: {path}")
        try:
            with zipfile.ZipFile(path, 'r') as zip_ref:
                for name in zip_ref.namelist():
                    with zip_ref.open(name) as f:
                        for line_number, line in enumerate(f.readlines()):
                            try:
                                content = line.decode(self.encoding)
                                yield self._create_document(
                                    content=content.strip(),
                                    line_number=line_number,
                                    file_name=name,
                                    source=f"{path}!{name}",
                                    file_type="zip-content"
                                )
                            except UnicodeDecodeError:
                                self.logger.warning(f"Cannot decode file {name} in ZIP archive {path}")
        except Exception as e:
            self.logger.error(f"Error processing ZIP file {path}: {str(e)}")

    @overrides
    def lazy_load(self) -> Iterator[Document]:
        """
        Lazy loading of documents line by line, optionally in batches.

        Args:
            batch_size (int): Number of documents to yield in each batch.

        Yields:
            Iterator[List[Document]]: Batches of Document objects.
        """
        pattern = '**/*' if self.recursive else '*'

        for path in self.file_path.glob(pattern):
            if path.is_file():
                # Check file extension
                if self.extension == ['*'] or path.suffix.lower().lstrip('.') in [ext.lower() for ext in self.extension]:
                    if self.zip_loader and path.suffix.lower() == '.zip':
                        documents = self._process_zip(path)
                    else:
                        documents = self._process_file(path)

                    for doc in documents:
                        yield doc

