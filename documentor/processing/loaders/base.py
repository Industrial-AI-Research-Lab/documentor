"""Base utilities for loaders."""

import time
from pathlib import Path
from typing import Callable, Set, Optional

from ...core.logging import get_logger

logger = get_logger(__name__)

# Try to import watchdog if available
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    logger.info("watchdog not installed - file auto-watching unavailable")
    WATCHDOG_AVAILABLE = False
    # Create type stubs
    Observer = None
    FileSystemEventHandler = object
    FileCreatedEvent = object
    FileModifiedEvent = object


class FileWatcher:
    """
    File change observer for automatic processing.
    
    Requires watchdog library installation.
    """
    
    def __init__(
        self,
        callback: Callable[[Path], None],
        supported_extensions: Set[str],
        watch_path: Path
    ):
        """
        Initialize observer.
        
        Args:
            callback: Callback function for processing new files
            supported_extensions: Supported file extensions
            watch_path: Path to watch
        """
        if not WATCHDOG_AVAILABLE:
            raise ImportError(
                "For file auto-watching, watchdog library is required. "
                "Install it: pip install watchdog"
            )
        
        self.callback = callback
        self.supported_extensions = supported_extensions
        self.watch_path = watch_path
        self._observer: Optional[Observer] = None
        self._event_handler = None
        
    def start_watching(self) -> None:
        """Start file watching."""
        if not WATCHDOG_AVAILABLE:
            logger.error("watchdog not available - watching impossible")
            return
            
        if self._observer is not None:
            logger.warning("Watching already started")
            return
        
        # Create event handler
        self._event_handler = _FileEventHandler(
            self.callback, 
            self.supported_extensions
        )
            
        self._observer = Observer()
        self._observer.schedule(self._event_handler, str(self.watch_path), recursive=True)
        self._observer.start()
        logger.info(f"Started watching {self.watch_path}")
        
    def stop_watching(self) -> None:
        """Stop file watching."""
        if self._observer is not None:
            self._observer.stop()
            self._observer.join()
            self._observer = None
            logger.info("Watching stopped")


class _FileEventHandler(FileSystemEventHandler):
    """Internal class for file system event handling."""
    
    def __init__(self, callback: Callable[[Path], None], supported_extensions: Set[str]):
        super().__init__()
        self.callback = callback
        self.supported_extensions = supported_extensions
    
    def on_created(self, event):
        """Handle file creation."""
        if WATCHDOG_AVAILABLE and isinstance(event, FileCreatedEvent):
            self._handle_file_event(Path(event.src_path), "created")
    
    def on_modified(self, event):
        """Handle file modification."""
        if WATCHDOG_AVAILABLE and isinstance(event, FileModifiedEvent):
            self._handle_file_event(Path(event.src_path), "modified")
    
    def _handle_file_event(self, file_path: Path, action: str):
        """Handle file event."""
        if file_path.suffix.lower() in self.supported_extensions:
            logger.info(f"File {action}: {file_path}")
            try:
                # Small delay for file write completion
                time.sleep(0.1)
                self.callback(file_path)
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        int: File size in bytes
    """
    try:
        return file_path.stat().st_size
    except (OSError, FileNotFoundError):
        return 0


def is_supported_file(file_path: Path, supported_extensions: Set[str]) -> bool:
    """
    Check if file is supported.
    
    Args:
        file_path: Path to file
        supported_extensions: Set of supported extensions
        
    Returns:
        bool: True if file is supported
    """
    return file_path.suffix.lower() in supported_extensions