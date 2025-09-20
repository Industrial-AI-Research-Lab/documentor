"""Text file parser without LangChain dependencies."""

from pathlib import Path
from typing import Set, Optional

from ...core.interfaces import BaseParser
from ...core.document import Document
from ...core.logging import get_logger
from documentor.core.env_config import env
from ...data.structures.metadata import Metadata
from ...data.structures.fragment import ParagraphFragment

logger = get_logger(__name__)


class TxtParser(BaseParser):
    """
    Parser for text files (.txt).
    
    Reads file line by line and creates single document with all lines as separate fragments.
    """
    
    def __init__(self, encoding: Optional[str] = None):
        """
        Initialize parser.
        
        Args:
            encoding: Encoding for reading files (defaults to env var or utf-8)
        """
        self.encoding = encoding or env.get_str("TXT_ENCODING", "utf-8")
    
    def supported_extensions(self) -> Set[str]:
        """Get supported extensions."""
        return {'.txt'}
    
    def parse(self, file_path: Path) -> Document:
        """
        Parse text file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            Document: Document with fragments for each line
            
        Raises:
            FileNotFoundError: If file not found
            ValueError: If file cannot be read
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        if file_path.suffix.lower() not in self.supported_extensions():
            raise ValueError(f"Unsupported file extension: {file_path.suffix}")
        
        logger.info(f"Parsing text file: {file_path}")
        
        # Create document metadata
        metadata = Metadata.from_path(
            file_path,
            processing_method="text_extraction"
        )
        
        fragments = []
        
        try:
            with open(file_path, 'r', encoding=self.encoding) as file:
                for line_num, line in enumerate(file, start=1):
                    # Remove newlines and extra spaces
                    line_content = line.rstrip('\n\r').strip()
                    
                    # Skip empty lines
                    if not line_content:
                        continue
                    
                    # Create fragment for each line
                    fragment = ParagraphFragment(
                        value=line_content,
                        page=str(line_num),  # Line number as page
                        id=f"line_{line_num}"
                    )
                    fragments.append(fragment)
                    
        except UnicodeDecodeError as e:
            logger.error(f"Error decoding file {file_path}: {e}")
            raise ValueError(f"Failed to decode file with encoding {self.encoding}: {e}")
        except IOError as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise ValueError(f"File reading error: {e}")
        
        logger.info(f"Created {len(fragments)} fragments from file {file_path}")
        
        # Create document
        document = Document(
            fragments=fragments,
            metadata=metadata
        )
        
        # Try to create hierarchical structure
        document.create_structure_from_headers()
        
        return document
