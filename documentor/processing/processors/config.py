"""Configuration for universal document processor."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Set

from ..pipelines.ocr.config import OCRPipelineConfig
from documentor.core.env_config import env


@dataclass
class ProcessingConfig:
    """
    Configuration for universal document processor.
    """
    
    # OCR configuration
    ocr_config: OCRPipelineConfig
    
    # Loading settings
    recursive: bool = True
    extract_archives: bool = True
    auto_watch: bool = False
    
    # File filters
    supported_extensions: Optional[Set[str]] = None
    max_file_size: Optional[int] = None  # in bytes
    
    # Processing settings
    create_hierarchy: bool = True
    batch_size: int = 10
    
    # Logging and output
    log_level: str = "INFO"
    output_directory: Optional[Path] = None
    save_processed_docs: bool = False
    
    @classmethod
    def create_default(
        cls,
        auto_watch: Optional[bool] = None,
        output_directory: Optional[Path] = None
    ) -> "ProcessingConfig":
        """
        Create default configuration.
        
        Args:
            auto_watch: Enable file auto-watching (overrides env var)
            output_directory: Directory for saving results (overrides env var)
            
        Returns:
            ProcessingConfig: Default configuration
        """
        ocr_config = OCRPipelineConfig.create_default()
        
        # Use environment variables if not explicitly provided
        if auto_watch is None:
            auto_watch = env.get_bool("AUTO_WATCH", False)
        
        if output_directory is None:
            output_directory = env.get_path("OUTPUT_DIRECTORY")
        
        # Parse supported extensions from env
        supported_extensions = None
        extensions_str = env.get("SUPPORTED_EXTENSIONS")
        if extensions_str:
            supported_extensions = set(ext.strip() for ext in extensions_str.split(","))
        
        # Convert max file size from MB to bytes
        max_file_size_mb = env.get_int("MAX_FILE_SIZE_MB")
        max_file_size = max_file_size_mb * 1024 * 1024 if max_file_size_mb else None
        
        return cls(
            ocr_config=ocr_config,
            recursive=env.get_bool("RECURSIVE", True),
            extract_archives=env.get_bool("EXTRACT_ARCHIVES", True),
            auto_watch=auto_watch,
            supported_extensions=supported_extensions,
            max_file_size=max_file_size,
            create_hierarchy=env.get_bool("CREATE_HIERARCHY", True),
            batch_size=env.get_int("BATCH_SIZE", 10),
            log_level=env.get_str("LOG_LEVEL", "INFO"),
            output_directory=output_directory,
            save_processed_docs=env.get_bool("SAVE_PROCESSED_DOCS", False)
        )
