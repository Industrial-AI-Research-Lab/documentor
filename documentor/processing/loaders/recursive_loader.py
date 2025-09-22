"""Recursive document loader without LangChain dependencies."""

import zipfile
from pathlib import Path
from typing import Iterator, Set, Optional, Dict

from ...core.interfaces import BaseLoader
from ...core.document import Document
from ...core.logging import get_logger
from .base import FileWatcher, get_file_size, is_supported_file

logger = get_logger(__name__)


class RecursiveDocumentLoader(BaseLoader):
    """
    Recursive document loader with ZIP archive support.
    
    Replaces old RecursiveLoader with LangChain dependency removed.
    """
    
    # Supported extensions
    SUPPORTED_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.docx'}
    ZIP_EXTENSIONS = {'.zip'}
    
    def __init__(
        self,
        parser_registry: Optional[Dict[str, object]] = None,
        extract_archives: bool = True,
        auto_watch: bool = False
    ):
        """
        Initialize loader.
        
        Args:
            parser_registry: Parser registry for different file types
            extract_archives: Whether to process ZIP archives
            auto_watch: Automatically watch for file changes
        """
        self.parser_registry = parser_registry or {}
        self.extract_archives = extract_archives
        self.auto_watch = auto_watch
        self._file_watcher: Optional[FileWatcher] = None
        
    def supported_extensions(self) -> Set[str]:
        """Get set of supported extensions."""
        extensions = self.SUPPORTED_EXTENSIONS.copy()
        if self.extract_archives:
            extensions.update(self.ZIP_EXTENSIONS)
        return extensions
    
    def load_file(self, file_path: Path) -> Document:
        """
        Load single file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Document: Loaded document
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type and select parser
        extension = file_path.suffix.lower()
        
        if extension in self.ZIP_EXTENSIONS and self.extract_archives:
            # ZIP archive processing - return empty document with metadata
            logger.info(f"Processing ZIP archive: {file_path}")
            return self._create_archive_document(file_path)
        
        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {extension}")
        
        # Find corresponding parser
        parser = self.parser_registry.get(extension)
        if parser is None:
            raise ValueError(f"Parser not found for extension: {extension}")
        
        logger.info(f"Parsing file: {file_path}")
        return parser.parse(file_path)
    
    def load_directory(self, directory_path: Path, recursive: bool = True) -> Iterator[Document]:
        """
        Load all supported files from directory.
        
        Args:
            directory_path: Path to directory
            recursive: Recursive traversal of subdirectories
            
        Yields:
            Document: Loaded documents
        """
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        if not directory_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        logger.info(f"Loading directory: {directory_path} (recursive={recursive})")
        
        # Setup auto-watching if needed
        if self.auto_watch:
            self._setup_file_watcher(directory_path)
        
        # Search pattern
        pattern = "**/*" if recursive else "*"
        
        for file_path in directory_path.glob(pattern):
            if file_path.is_file():
                try:
                    # Check if file is supported
                    if is_supported_file(file_path, self.supported_extensions()):
                        yield self.load_file(file_path)
                    
                    # Additionally process ZIP archives
                    if (file_path.suffix.lower() in self.ZIP_EXTENSIONS 
                        and self.extract_archives):
                        yield from self._process_zip_archive(file_path)
                        
                except Exception as e:
                    logger.error(f"Error loading file {file_path}: {e}")
                    continue
    
    def _create_archive_document(self, archive_path: Path) -> Document:
        """
        Create document for ZIP archive.
        
        Args:
            archive_path: Path to archive
            
        Returns:
            Document: Document with archive metadata
        """
        from ..structuries.metadata import Metadata
        from ..structuries.fragment.text import ParagraphFragment
        
        metadata = Metadata.from_path(
            archive_path,
            processing_method="archive_metadata"
        )
        
        # Create fragment with archive information
        fragment = ParagraphFragment(
            value=f"ZIP archive: {archive_path.name}",
            page="archive_info"
        )
        
        return Document(fragments=[fragment], metadata=metadata)
    
    def _process_zip_archive(self, archive_path: Path) -> Iterator[Document]:
        """
        Process ZIP archive and extract supported files.
        
        Args:
            archive_path: Path to ZIP archive
            
        Yields:
            Document: Documents from archive
        """
        logger.info(f"Extracting files from archive: {archive_path}")
        
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                for file_info in zip_ref.filelist:
                    if file_info.is_dir():
                        continue
                    
                    # Check file extension in archive
                    file_path = Path(file_info.filename)
                    extension = file_path.suffix.lower()
                    
                    if extension not in self.SUPPORTED_EXTENSIONS:
                        continue
                    
                    # Extract file to temporary area
                    try:
                        file_data = zip_ref.read(file_info.filename)
                        yield self._process_archive_file(
                            file_path, file_data, archive_path
                        )
                    except Exception as e:
                        logger.error(f"Error extracting {file_info.filename} from {archive_path}: {e}")
                        continue
                        
        except zipfile.BadZipFile:
            logger.error(f"Corrupted ZIP archive: {archive_path}")
        except Exception as e:
            logger.error(f"Error processing archive {archive_path}: {e}")
    
    def _process_archive_file(
        self, 
        file_path: Path, 
        file_data: bytes, 
        archive_path: Path
    ) -> Document:
        """
        Process file from archive.
        
        Args:
            file_path: Path to file inside archive
            file_data: File data
            archive_path: Path to archive
            
        Returns:
            Document: Processed document
        """
        from ..structuries.metadata import Metadata
        from ..structuries.fragment.text import ParagraphFragment
        
        extension = file_path.suffix.lower()
        
        # Create metadata for file from archive
        metadata = Metadata(
            name=file_path.name,
            extension=extension,
            file_path=f"{archive_path}!{file_path}",  # Special format for archives
            file_size=len(file_data),
            processing_method="archive_extraction"
        )
        
        # Simple processing of text files from archive
        if extension == '.txt':
            try:
                text_content = file_data.decode('utf-8')
                fragments = []
                for line_num, line in enumerate(text_content.splitlines()):
                    if line.strip():  # Skip empty lines
                        fragment = ParagraphFragment(
                            value=line.strip(),
                            page=str(line_num + 1)
                        )
                        fragments.append(fragment)
                
                return Document(fragments=fragments, metadata=metadata)
            except UnicodeDecodeError:
                logger.warning(f"Failed to decode text file {file_path} from archive")
        
        # For other file types create stub
        fragment = ParagraphFragment(
            value=f"File from archive: {file_path.name} (size: {len(file_data)} bytes)",
            page="archive_file"
        )
        
        return Document(fragments=[fragment], metadata=metadata)
    
    def _setup_file_watcher(self, watch_path: Path) -> None:
        """
        Setup file watching.
        
        Args:
            watch_path: Path to watch
        """
        if self._file_watcher is not None:
            return
        
        def process_new_file(file_path: Path) -> None:
            """Handle new or modified file."""
            try:
                document = self.load_file(file_path)
                logger.info(f"Automatically processed file: {file_path}")
                # Here callback can be added for document forwarding
            except Exception as e:
                logger.error(f"Error auto-processing file {file_path}: {e}")
        
        try:
            self._file_watcher = FileWatcher(
                callback=process_new_file,
                supported_extensions=self.supported_extensions(),
                watch_path=watch_path
            )
            self._file_watcher.start_watching()
        except ImportError as e:
            logger.warning(f"Auto-watching unavailable: {e}")
            self._file_watcher = None
    
    def stop_watching(self) -> None:
        """Stop file watching."""
        if self._file_watcher is not None:
            self._file_watcher.stop_watching()
            self._file_watcher = None