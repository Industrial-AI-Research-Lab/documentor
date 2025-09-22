"""
Structured storage for processed documents.
"""

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image

from ..core.document import Document
from .document_serializer import DocumentSerializer


logger = logging.getLogger(__name__)


class StructuredDocumentStorage:
    """
    Class for structured storage of processed documents.
    
    Creates organized folder structure with metadata, fragments,
    hierarchy and images. Supports indexing and deduplication.
    """
    
    def __init__(self, output_directory: Path):
        """
        Initialize storage.
        
        Args:
            output_directory: Path to directory for saving results
        """
        self.output_directory = Path(output_directory)
        self.documents_dir = self.output_directory / "documents"
        self.logs_dir = self.output_directory / "logs"
        self.index_file = self.output_directory / "index.json"
        self.stats_file = self.output_directory / "processing_stats.json"
        
        self.serializer = DocumentSerializer()
        
        # Create folder structure
        self._setup_directories()
        
        # Load existing index
        self.index = self._load_index()
        self.stats = self._load_stats()
    
    def _setup_directories(self) -> None:
        """Create necessary directories."""
        self.output_directory.mkdir(exist_ok=True)
        self.documents_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        logger.info(f"Storage structure created: {self.output_directory}")
    
    def _load_index(self) -> Dict[str, Any]:
        """Load document index."""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading index: {e}")
        
        return {
            "total_documents": 0,
            "last_updated": datetime.now().isoformat(),
            "documents": {},
            "file_hashes": {}
        }
    
    def _load_stats(self) -> Dict[str, Any]:
        """Load processing statistics."""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading statistics: {e}")
        
        return {
            "total_processed": 0,
            "total_errors": 0,
            "processing_times": [],
            "file_types": {},
            "last_reset": datetime.now().isoformat()
        }
    
    def _save_index(self) -> None:
        """Save document index."""
        self.index["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def _save_stats(self) -> None:
        """Save statistics."""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving statistics: {e}")
    
    def check_duplicate(self, file_path: Path) -> Optional[str]:
        """
        Check for duplication by file hash.
        
        Args:
            file_path: Path to file for checking
            
        Returns:
            Document ID if duplicate found, otherwise None
        """
        file_hash = self.serializer.calculate_file_hash(file_path)
        if file_hash and file_hash in self.index["file_hashes"]:
            return self.index["file_hashes"][file_hash]
        return None
    
    def save_document(
        self,
        document: Document,
        original_file_path: Path,
        processing_method: str,
        processing_start: datetime,
        processing_end: datetime,
        save_fragment_images: bool = True
    ) -> str:
        """
        Save document in structured format.
        
        Args:
            document: Processed document
            original_file_path: Path to source file
            processing_method: Processing method (txt, pdf_ocr, image_ocr)
            processing_start: Processing start time
            processing_end: Processing end time
            save_fragment_images: Whether to save fragment images
            
        Returns:
            ID of created document
        """
        
        # Check for duplicates
        duplicate_id = self.check_duplicate(original_file_path)
        if duplicate_id:
            logger.info(f"File already processed: {original_file_path.name} (ID: {duplicate_id})")
            return duplicate_id
        
        # Generate document ID
        document_id = self.serializer.generate_document_id()
        document_dir = self.documents_dir / document_id
        document_dir.mkdir(exist_ok=True)
        
        logger.info(f"Saving document {document_id} from file {original_file_path.name}")
        
        try:
            # 1. Save document metadata
            metadata = self.serializer.serialize_document_metadata(
                document, document_id, original_file_path,
                processing_start, processing_end, processing_method
            )
            self.serializer.save_json(metadata, document_dir / "document.json")
            
            # 2. Save fragments
            fragments_data = self.serializer.serialize_fragments(
                document, document_id, save_fragment_images
            )
            self.serializer.save_json(fragments_data, document_dir / "fragments.json")
            
            # 3. Save structure
            structure_data = self.serializer.serialize_structure(document)
            self.serializer.save_json(structure_data, document_dir / "structure.json")
            
            # 4. Save fragment images
            if save_fragment_images:
                self._save_fragment_images(document, document_dir)
            
            # 5. Update index
            self._update_index(document_id, original_file_path, metadata)
            
            # 6. Update statistics
            self._update_stats(processing_method, processing_start, processing_end)
            
            logger.info(f"Document {document_id} successfully saved")
            return document_id
            
        except Exception as e:
            logger.error(f"Error saving document {document_id}: {e}")
            # Remove partially created folder
            if document_dir.exists():
                shutil.rmtree(document_dir, ignore_errors=True)
            raise
    
    def _save_fragment_images(self, document: Document, document_dir: Path) -> None:
        """Save fragment images."""
        images_dir = document_dir / "fragment_images"
        images_dir.mkdir(exist_ok=True)
        
        saved_count = 0
        for i, fragment in enumerate(document.fragments()):
            # Find image in fragment
            fragment_image = None
            if hasattr(fragment, 'image') and fragment.image:
                fragment_image = fragment.image
            elif hasattr(fragment, 'value') and hasattr(fragment.value, 'save'):  # PIL Image check
                fragment_image = fragment.value
            
            if fragment_image:
                try:
                    fragment_id = f"fragment_{i+1:03d}"
                    image_path = images_dir / f"{fragment_id}.png"
                    
                    # Save image
                    if isinstance(fragment_image, Image.Image):
                        fragment_image.save(image_path, "PNG")
                        saved_count += 1
                        logger.debug(f"Saved fragment image {fragment_id}")
                    else:
                        logger.warning(f"Unsupported image type for fragment {fragment_id}: {type(fragment_image)}")
                        
                except Exception as e:
                    logger.error(f"Error saving fragment image {i+1}: {e}")
        
        if saved_count > 0:
            logger.info(f"Saved {saved_count} fragment images")
        else:
            logger.info("No fragment images found for saving")
    
    def _update_index(self, document_id: str, original_file_path: Path, metadata: Dict[str, Any]) -> None:
        """Update document index."""
        file_hash = metadata["original_file"]["md5_hash"]
        
        self.index["documents"][document_id] = {
            "original_file": original_file_path.name,
            "processed_at": metadata["processing"]["completed_at"],
            "status": metadata["processing"]["status"],
            "fragments_count": metadata["content_summary"]["total_fragments"],
            "file_size": metadata["original_file"]["size_bytes"],
            "processing_method": metadata["processing"]["method"]
        }
        
        if file_hash:
            self.index["file_hashes"][file_hash] = document_id
        
        self.index["total_documents"] = len(self.index["documents"])
        self._save_index()
    
    def _update_stats(self, processing_method: str, start_time: datetime, end_time: datetime) -> None:
        """Update processing statistics."""
        duration = (end_time - start_time).total_seconds()
        
        self.stats["total_processed"] += 1
        self.stats["processing_times"].append(duration)
        
        # Limit processing time history
        if len(self.stats["processing_times"]) > 1000:
            self.stats["processing_times"] = self.stats["processing_times"][-500:]
        
        # Statistics by file types
        self.stats["file_types"][processing_method] = self.stats["file_types"].get(processing_method, 0) + 1
        
        self._save_stats()
    
    def get_document_info(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get document information."""
        if document_id in self.index["documents"]:
            return self.index["documents"][document_id]
        return None
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """Get list of all documents."""
        return [
            {**info, "document_id": doc_id}
            for doc_id, info in self.index["documents"].items()
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics."""
        stats = self.stats.copy()
        
        # Add computed metrics
        if stats["processing_times"]:
            stats["avg_processing_time"] = sum(stats["processing_times"]) / len(stats["processing_times"])
            stats["min_processing_time"] = min(stats["processing_times"])
            stats["max_processing_time"] = max(stats["processing_times"])
        
        stats["total_documents"] = self.index["total_documents"]
        stats["success_rate"] = 1.0 - (stats["total_errors"] / max(stats["total_processed"], 1))
        
        return stats
    
    def cleanup_old_documents(self, days_old: int = 30) -> int:
        """
        Cleanup old documents.
        
        Args:
            days_old: Age of documents in days for deletion
            
        Returns:
            Number of deleted documents
        """
        # This function can be implemented in the future
        # for automatic cleanup of old documents
        pass
