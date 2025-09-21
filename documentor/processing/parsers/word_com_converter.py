"""
Microsoft Word COM-based DOC to DOCX converter.

Uses Microsoft Word COM interface to convert DOC files to DOCX format
for full-featured parsing with python-docx.
"""

import tempfile
import os
from pathlib import Path
from typing import Optional

from ...core.logging import get_logger

logger = get_logger(__name__)


class WordCOMConverter:
    """
    Converts DOC files to DOCX using Microsoft Word COM interface.
    
    This provides reliable conversion for DOC files on Windows systems
    with Microsoft Word installed.
    """
    
    def __init__(self):
        """Initialize the Word COM converter."""
        self.word_app = None
        self.is_available = self._check_word_availability()
        if self.is_available:
            logger.info("Word COM converter initialized")
        else:
            logger.warning("Microsoft Word not available via COM")
    
    def _check_word_availability(self) -> bool:
        """Check if Microsoft Word is available via COM."""
        try:
            import win32com.client
            # Try to create Word application
            word_app = win32com.client.Dispatch("Word.Application")
            word_app.Visible = False
            word_app.Quit()
            return True
        except Exception as e:
            logger.debug(f"Word COM not available: {e}")
            return False
    
    def convert_doc_to_docx(self, doc_path: Path, output_dir: Optional[Path] = None) -> Path:
        """
        Convert DOC file to DOCX using Microsoft Word COM.
        
        Args:
            doc_path: Path to input DOC file
            output_dir: Directory for output DOCX file (optional, uses temp dir if not provided)
            
        Returns:
            Path to the created DOCX file
            
        Raises:
            FileNotFoundError: If DOC file not found
            ValueError: If conversion fails
            RuntimeError: If Word COM not available
        """
        if not self.is_available:
            raise RuntimeError("Microsoft Word COM not available")
        
        if not doc_path.exists():
            raise FileNotFoundError(f"DOC file not found: {doc_path}")
        
        if not doc_path.is_file():
            raise ValueError(f"Path is not a file: {doc_path}")
        
        if doc_path.suffix.lower() != '.doc':
            raise ValueError(f"File is not a DOC file: {doc_path}")
        
        logger.info(f"Converting DOC to DOCX using Word COM: {doc_path}")
        
        try:
            import win32com.client
            
            # Determine output directory
            if output_dir is None:
                output_dir = Path(tempfile.gettempdir()) / "documentor_word_conversion"
                output_dir.mkdir(exist_ok=True)
            else:
                output_dir.mkdir(parents=True, exist_ok=True)
            
            # Create Word application
            word_app = win32com.client.Dispatch("Word.Application")
            word_app.Visible = False
            
            try:
                # Open DOC file
                doc = word_app.Documents.Open(str(doc_path.absolute()))
                
                # Determine output path
                output_path = output_dir / f"{doc_path.stem}.docx"
                
                # Save as DOCX (FileFormat=16 for DOCX)
                doc.SaveAs(str(output_path.absolute()), FileFormat=16)
                
                # Close document
                doc.Close()
                
                logger.info(f"Successfully converted DOC to DOCX: {output_path}")
                return output_path
                
            finally:
                # Quit Word application
                word_app.Quit()
                
        except Exception as e:
            logger.error(f"Error converting DOC file {doc_path}: {e}")
            raise ValueError(f"Failed to convert DOC file: {e}")
    
    def cleanup_temp_files(self, temp_dir: Path) -> None:
        """
        Clean up temporary conversion files.
        
        Args:
            temp_dir: Directory to clean up
        """
        try:
            if temp_dir.exists():
                import shutil
                shutil.rmtree(temp_dir)
                logger.debug(f"Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            logger.warning(f"Failed to clean up temporary directory {temp_dir}: {e}")
