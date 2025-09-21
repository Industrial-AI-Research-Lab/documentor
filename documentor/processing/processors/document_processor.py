"""Universal document processor - main pipeline."""

import json
from pathlib import Path
from typing import Iterator, List, Optional, Callable, Dict, Any

from ...core.document import Document
from ...core.logging import get_logger, setup_logging
from ..loaders.recursive_loader import RecursiveDocumentLoader
from ..parsers.registry import ParserRegistry
from .config import ProcessingConfig

logger = get_logger(__name__)


class DocumentProcessor:
    """
    Universal document processor.
    
    Main pipeline that combines:
    - Recursive loader with ZIP support
    - Automatic parser selection
    - OCR processing (dots.ocr + Qwen2.5)
    - Hierarchical structure creation
    - File auto-watching
    """
    
    def __init__(
        self,
        config: Optional[ProcessingConfig] = None,
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ):
        """
        Initialize processor.
        
        Args:
            config: Processing configuration
            progress_callback: Callback for progress reporting (message, current, total)
        """
        self.config = config or ProcessingConfig.create_default()
        self.progress_callback = progress_callback
        
        # Setup logging
        setup_logging(
            level=self.config.log_level,
            log_file=self.config.output_directory / "processing.log" if self.config.output_directory else None
        )
        
        # Create components
        self.parser_registry = ParserRegistry(self.config.ocr_config)
        self.loader = RecursiveDocumentLoader(
            parser_registry=self._create_parser_dict(),
            extract_archives=self.config.extract_archives,
            auto_watch=self.config.auto_watch
        )
        
        logger.info("DocumentProcessor initialized")
    
    def _create_parser_dict(self) -> Dict[str, object]:
        """Create parser dictionary for loader."""
        parser_dict = {}
        for ext in self.parser_registry.supported_extensions():
            parser_dict[ext] = self.parser_registry.get_parser(Path(f"dummy{ext}"))
        return parser_dict
    
    def process_file(self, file_path: Path) -> Document:
        """
        Process single file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Document: Processed document
        """
        logger.info(f"Processing file: {file_path}")
        
        # Check file size if limit is set
        if self.config.max_file_size:
            file_size = file_path.stat().st_size
            if file_size > self.config.max_file_size:
                raise ValueError(f"File too large: {file_size} bytes > {self.config.max_file_size}")
        
        # Load document
        document = self.loader.load_file(file_path)
        
        # Create hierarchy if needed
        if self.config.create_hierarchy:
            try:
                structure = document.create_structure_from_headers()
                if structure:
                    logger.info(f"Created hierarchical structure with {len(structure.fragments)} fragments")
            except AttributeError:
                # Method doesn't exist yet, skip for now
                logger.debug("create_structure_from_headers method not available, skipping")
        
        # Save document if needed
        if self.config.save_processed_docs and self.config.output_directory:
            self._save_document(document, file_path)
        
        logger.info(f"File processed: {len(document.fragments())} fragments")
        return document
    
    def process_directory(
        self, 
        directory_path: Path,
        recursive: Optional[bool] = None
    ) -> Iterator[Document]:
        """
        Process directory with files.
        
        Args:
            directory_path: Path to directory
            recursive: Recursive processing (default from config)
            
        Yields:
            Document: Processed documents
        """
        if recursive is None:
            recursive = self.config.recursive
        
        logger.info(f"Processing directory: {directory_path} (recursive={recursive})")
        
        # Count total files for progress
        total_files = sum(1 for _ in self._get_supported_files(directory_path, recursive))
        current_file = 0
        
        # Process files in batches
        batch = []
        for document in self.loader.load_directory(directory_path, recursive):
            current_file += 1
            
            # Notify about progress
            if self.progress_callback:
                self.progress_callback(
                    f"Processing file {current_file}/{total_files}",
                    current_file,
                    total_files
                )
            
            # Create hierarchy if needed
            if self.config.create_hierarchy:
                try:
                    document.create_structure_from_headers()
                except AttributeError:
                    # Method doesn't exist yet, skip for now
                    logger.debug("create_structure_from_headers method not available, skipping")
            
            batch.append(document)
            
            # Return batch when it's full
            if len(batch) >= self.config.batch_size:
                yield from batch
                batch = []
        
        # Return remaining documents
        if batch:
            yield from batch
        
        logger.info(f"Directory processing completed: {current_file} files")
    
    def process_directory_to_list(
        self, 
        directory_path: Path,
        recursive: Optional[bool] = None
    ) -> List[Document]:
        """
        Process directory and return list of all documents.
        
        Args:
            directory_path: Path to directory
            recursive: Recursive processing
            
        Returns:
            List[Document]: List of all processed documents
        """
        return list(self.process_directory(directory_path, recursive))
    
    def start_watching(self, directory_path: Path) -> None:
        """
        Start auto-watching for changes in directory.
        
        Args:
            directory_path: Path to directory for watching
        """
        logger.info(f"Starting auto-watching for directory: {directory_path}")
        
        # Setup callback for new file processing
        def process_new_file(file_path: Path) -> None:
            try:
                document = self.process_file(file_path)
                logger.info(f"Automatically processed new file: {file_path}")
                
                # Callback can be added for document forwarding
                if hasattr(self, 'new_file_callback') and self.new_file_callback:
                    self.new_file_callback(document)
                    
            except Exception as e:
                logger.error(f"Error auto-processing file {file_path}: {e}")
        
        # Setup auto-watching in loader
        if not self.loader._file_watcher:
            self.loader._setup_file_watcher(directory_path)
        
        # Replace callback
        if self.loader._file_watcher:
            self.loader._file_watcher.callback = process_new_file
    
    def stop_watching(self) -> None:
        """Stop auto-watching."""
        logger.info("Stopping auto-watching")
        self.loader.stop_watching()
    
    def get_supported_extensions(self) -> set[str]:
        """Get list of supported extensions."""
        return self.parser_registry.supported_extensions()
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        Returns:
            Dict[str, Any]: Processor statistics
        """
        return {
            "supported_extensions": list(self.get_supported_extensions()),
            "parsers": self.parser_registry.get_parser_info(),
            "config": {
                "recursive": self.config.recursive,
                "extract_archives": self.config.extract_archives,
                "auto_watch": self.config.auto_watch,
                "create_hierarchy": self.config.create_hierarchy,
                "batch_size": self.config.batch_size,
            }
        }
    
    def _get_supported_files(self, directory_path: Path, recursive: bool) -> Iterator[Path]:
        """Get list of supported files in directory."""
        pattern = "**/*" if recursive else "*"
        supported_extensions = self.get_supported_extensions()
        
        for file_path in directory_path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                yield file_path
    
    def _save_document(self, document: Document, original_path: Path) -> None:
        """
        Save processed document.
        
        Args:
            document: Document to save
            original_path: Original file path
        """
        if not self.config.output_directory:
            return
        
        # Create directory if it doesn't exist
        self.config.output_directory.mkdir(parents=True, exist_ok=True)
        
        # Create output filename
        output_name = original_path.stem + "_processed.json"
        output_path = self.config.output_directory / output_name
        
        try:
            # Create serializable document representation
            doc_data = {
                "metadata": {
                    "file_path": document.metadata.file_path,
                    "file_size": document.metadata.file_size,
                    "processing_method": document.metadata.processing_method,
                    "params": document.metadata.params,
                },
                "fragments": [
                    {
                        "type": type(fragment).__name__,
                        "value": str(fragment.value),
                        "page": fragment.page,
                        "id": fragment.id,
                    }
                    for fragment in document.fragments()
                ],
                "total_fragments": len(document.fragments())
            }
            
            # Save to JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(doc_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Document saved: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving document {output_path}: {e}")
    
    def set_new_file_callback(self, callback: Callable[[Document], None]) -> None:
        """
        Set callback for processing new files during auto-watching.
        
        Args:
            callback: Function to call when processing new file
        """
        self.new_file_callback = callback
