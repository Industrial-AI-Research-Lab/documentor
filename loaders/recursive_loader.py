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
                 log_level: int = logging.INFO,
                 **kwargs):
        """
        Initialize the RecursiveLoader.

        Args:
            file_path (Union[str, Path]): Path to the directory or file.
            extension (List[str], optional): List of file extensions to load. Defaults to all files.
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

        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        logging.basicConfig(level=log_level)

        # Initialize logs
        self._logs = {
            "info": [],
            "warning": [],
            "error": []
        }

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

    def _should_process(self, path: Path) -> bool:
        """
        Check if the file should be processed based on its extension.

        Args:
            path (Path): Path to the file.

        Returns:
            bool: True if the file should be processed, False otherwise.
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
        self.logger.info(f"Чтение файла: {path}")
        self._logs["info"].append(f"Чтение файла: {path}")
        try:
            with open(path, 'r') as f:
                for line_number, line in enumerate(f):
                    yield self._create_document(
                        content=line.strip(),
                        line_number=line_number,
                        file_name=path.name,
                        source=str(path),
                        file_type=path.suffix
                    )
        except UnicodeDecodeError:
            self.logger.warning(f"Невозможно декодировать файл {path}")
            self._logs["warning"].append(f"Невозможно декодировать файл {path}")
        except Exception as e:
            self.logger.error(f"Ошибка при чтении файла {path}: {str(e)}")
            self._logs["error"].append(f"Ошибка при чтении файла {path}: {str(e)}")

    def _process_zip(self, path: Path) -> Iterator[Document]:
        """
        Process a ZIP file and yield Document objects for each line in each file.

        Args:
            path (Path): Path to the ZIP file.

        Yields:
            Iterator[Document]: Document objects.
        """
        self.logger.info(f"Обработка ZIP архива: {path}")
        self._logs["info"].append(f"Обработка ZIP архива: {path}")
        try:
            with zipfile.ZipFile(path, 'r') as zip_ref:
                for name in zip_ref.namelist():
                    try:
                        with zip_ref.open(name) as f:
                            for line_number, line in enumerate(f):
                                try:
                                    content = line.decode()
                                    yield self._create_document(
                                        content=content.strip(),
                                        line_number=line_number,
                                        file_name=name,
                                        source=f"{path}!{name}",
                                        file_type="zip-content"
                                    )
                                except UnicodeDecodeError:
                                    self.logger.warning(f"Невозможно декодировать файл {name} в ZIP архиве {path}")
                                    self._logs["warning"].append(f"Невозможно декодировать файл {name} в ZIP архиве {path}")
                    except Exception as e:
                        self.logger.error(f"Ошибка при чтении файла {name} в ZIP архиве {path}: {str(e)}")
                        self._logs["error"].append(f"Ошибка при чтении файла {name} в ZIP архиве {path}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Ошибка при обработке ZIP файла {path}: {str(e)}")
            self._logs["error"].append(f"Ошибка при обработке ZIP файла {path}: {str(e)}")

    @overrides
    def lazy_load(self) -> Iterator[Document]:
        """
        Lazy loading of documents line by line.

        Yields:
            Iterator[Document]: Document objects.
        """
        pattern = '**/*' if self.recursive else '*'

        for path in self.file_path.glob(pattern):
            if path.is_file() and self._should_process(path):
                documents = (
                    self._process_zip(path) if self.zip_loader and path.suffix.lower() == '.zip' else self._process_file(path)
                )

                for doc in documents:
                    yield doc

    @property
    @overrides
    def logs(self) -> dict[str, list[str]]:
        """
        Returns the logs collected during processing.

        Returns:
            dict[str, list[str]]: A dictionary containing lists of log messages for 'info', 'warning', and 'error'.
        """
        return self._logs

