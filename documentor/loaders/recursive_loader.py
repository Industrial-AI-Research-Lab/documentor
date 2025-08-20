import zipfile
from pathlib import Path
from typing import Iterator, Optional

from langchain_core.documents import Document
from langchain_core.documents.base import Blob
from overrides import overrides

from documentor.loaders.base import BaseLoader
from documentor.parsers.extension_mapping import ExtensionMapping
from documentor.parsers.extensions import ZIP_EXTENSIONS, DocExtension


def get_extension(path: Path) -> str:
    """
    Get the file extension including leading dot (e.g., '.txt').

    Args:
        path (Path): Path to the file.

    Returns:
        str: File extension with leading dot.
    """
    return path.suffix.lower()


class RecursiveLoader(BaseLoader):
    """
    Loader for recursive directory traversal and optional ZIP file processing.

    Attributes:
        path (str | Path): Path to the directory or file.
        is_recursive (bool): Whether to traverse directories recursively.
        use_unzip (bool): Whether to process ZIP files.
    """

    def __init__(
            self,
            path: str | Path,
            extension: Optional[list[str]] = None,
            extension_mapping: Optional[ExtensionMapping] = None,
            is_recursive: bool = True,
            use_unzip: bool = False,
            **kwargs
    ):
        """
        Initialize the RecursiveLoader.

        Args:
            path (Union[str, Path]): Path to the directory or file.
            extension (Optional[list[str]]): A whitelist of file extensions to process (e.g., ["txt", "md", "zip"]).
            extension_mapping (Optional[ExtensionMapping]): Mapping of file extensions to parsers. Defaults to None.
            is_recursive (bool): Whether to traverse directories recursively. Defaults to True.
            use_unzip (bool): Whether to process ZIP files. Defaults to False.
        """
        super().__init__(path, extension_mapping, **kwargs)

        self.is_recursive = is_recursive
        self.use_unzip = use_unzip
        # Normalize and store allowed extensions for quick checks
        self._allowed_extensions: set[DocExtension] | None = None
        if extension is not None:
            self._allowed_extensions = set()
            for ext in extension:
                # Accept values both with and without leading dot
                self._allowed_extensions.add(DocExtension.from_string(ext))
        # Parsers are now selected dynamically through extension_mapping, so creating them here is not necessary.

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
        # TODO: decide which metadata should be used
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
        Check if the file has a valid extension considering allowed list and known parsers.

        Args:
            path (Path): Path to the file.

        Returns:
            bool: True if the file has a valid extension, False otherwise.
        """
        ext = DocExtension.from_string(path.suffix)
        # If a whitelist is provided, only allow those
        if self._allowed_extensions is not None and ext not in self._allowed_extensions:
            return False
        # Consider as valid if a parser exists OR it's a plain text-like file we handle inline (txt/md)
        return self._extension_mapping.is_valid_extension(ext) or ext in {DocExtension.txt, DocExtension.md}

    def _process_file(self, path: Path) -> Iterator[Document]:
        """
        Process a single file and yield Document objects line by line.

        Args:
            path (Path): Path to the file.

        Yields:
            Iterator[Document]: Document objects.
        """
        self._logs.add_info(f"Reading file: {path}")
        try:
            blob = Blob.from_path(path)
            file_extension = DocExtension.from_string(path.suffix)
            # Special handling for plain text files to return one Document per line
            if file_extension in {DocExtension.txt, DocExtension.md}:
                text = blob.as_string()
                for line_number, line in enumerate(text.splitlines()):
                    yield self._create_document(
                        content=line.strip(),
                        line_number=line_number,
                        file_name=path.name,
                        source=str(path),
                        file_type=file_extension.value.lstrip('.')
                    )
            else:
                parser = self._extension_mapping.get_parser(file_extension)
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
        pattern = '**/*' if self.is_recursive else '*'
        for path in self.path.glob(pattern):
            if path.is_dir():
                continue

            documents: Iterator[Document] = iter([])
            ext = DocExtension.from_string(get_extension(path))
            # Process regular files if extension is allowed
            if self._is_valid_extension(path):
                documents = self._process_file(path)
            # Process archives if enabled and allowed
            elif self.use_unzip and ext in ZIP_EXTENSIONS:
                # Respect whitelist if provided
                if self._allowed_extensions is None or ext in self._allowed_extensions:
                    documents = self._process_zip(path)

            for document in documents:
                yield document
