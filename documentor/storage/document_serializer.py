"""
Document and fragment serialization to JSON format.
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from ..core.document import Document
from ..data.structures.fragment import Fragment


class DocumentSerializer:
    """Class for serializing documents to structured JSON format."""
    
    @staticmethod
    def generate_document_id() -> str:
        """Generate unique document ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"doc_{timestamp}_{hash(datetime.now()) % 1000:03d}"
    
    @staticmethod
    def calculate_file_hash(file_path: Path) -> str:
        """Calculate MD5 hash of file."""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
    
    def serialize_document_metadata(
        self, 
        document: Document, 
        document_id: str,
        original_file_path: Path,
        processing_start: datetime,
        processing_end: datetime,
        processing_method: str
    ) -> Dict[str, Any]:
        """Serialize document metadata."""
        
        # Count fragment types
        fragment_types = {}
        total_text_length = 0
        
        for fragment in document.fragments():
            fragment_type = fragment.__class__.__name__.lower().replace('fragment', '')
            fragment_types[fragment_type] = fragment_types.get(fragment_type, 0) + 1
            
            if hasattr(fragment, 'content') and fragment.content:
                total_text_length += len(str(fragment.content))
        
        file_stats = original_file_path.stat() if original_file_path.exists() else None
        
        return {
            "document_id": document_id,
            "original_file": {
                "path": str(original_file_path),
                "name": original_file_path.name,
                "extension": original_file_path.suffix.lower().lstrip('.'),
                "size_bytes": file_stats.st_size if file_stats else 0,
                "created_at": datetime.fromtimestamp(file_stats.st_ctime).isoformat() if file_stats else None,
                "md5_hash": self.calculate_file_hash(original_file_path)
            },
            "processing": {
                "method": processing_method,
                "started_at": processing_start.isoformat(),
                "completed_at": processing_end.isoformat(),
                "duration_seconds": int((processing_end - processing_start).total_seconds()),
                "status": "success"
            },
            "content_summary": {
                "total_fragments": len(document.fragments()),
                "fragment_types": fragment_types,
                "total_text_length": total_text_length,
                "language": getattr(document.metadata, 'language', 'unknown') if document.metadata else 'unknown'
            }
        }
    
    def serialize_fragments(
        self, 
        document: Document,
        document_id: str,
        save_images: bool = True
    ) -> Dict[str, Any]:
        """Serialize all document fragments."""
        
        fragments_data = []
        
        for i, fragment in enumerate(document.fragments()):
            fragment_id = f"fragment_{i+1:03d}"
            
            # Extract data from fragment
            content = getattr(fragment, 'value', None) or getattr(fragment, 'content', None)
            
            # For ImageFragment don't show content as text (it's PIL Image)
            if hasattr(content, 'save'):  # PIL Image check
                content = f"[IMAGE: {content.size[0]}x{content.size[1]}]" if hasattr(content, 'size') else "[IMAGE]"
            
            # Extract bbox and confidence from style if available
            style = getattr(fragment, 'style', {}) or {}
            bbox = getattr(fragment, 'bbox', None) or style.get('bbox')
            confidence = getattr(fragment, 'confidence', None) or style.get('confidence')
            
            # Try to determine level
            level = getattr(fragment, 'level', None) or style.get('level')
            
            # For headers, try to determine default level
            fragment_type = fragment.__class__.__name__.lower()
            if level is None and 'header' in fragment_type:
                if 'title' in fragment_type:
                    level = 1  # TitleFragment = level 1
                else:
                    level = 2  # HeaderFragment = level 2
            
            # Determine page (default 1 for images)
            page = getattr(fragment, 'page', None)
            if page is None:
                page = 1  # Default first page
            
            # Basic fragment data
            fragment_data = {
                "fragment_id": fragment_id,
                "type": fragment.__class__.__name__.lower().replace('fragment', ''),
                "content": content,
                "bbox": bbox,
                "page": page,
                "confidence": confidence,
                "level": level,
                "order_index": i,
                "metadata": {},
                "image_file": None
            }
            
            # Additional metadata from metadata object
            if hasattr(fragment, 'metadata') and fragment.metadata:
                # Copy metadata, excluding complex objects
                for key, value in fragment.metadata.__dict__.items():
                    if isinstance(value, (str, int, float, bool, list, dict)) or value is None:
                        fragment_data["metadata"][key] = value
            
            # Additional metadata from style
            if style:
                for key, value in style.items():
                    if key not in ['bbox', 'confidence'] and (isinstance(value, (str, int, float, bool, list, dict)) or value is None):
                        fragment_data["metadata"][key] = value
            
            # Specific fields for different fragment types
            if hasattr(fragment, 'font_size'):
                fragment_data["metadata"]["font_size"] = fragment.font_size
            if hasattr(fragment, 'is_bold'):
                fragment_data["metadata"]["is_bold"] = fragment.is_bold
            if hasattr(fragment, 'classification'):
                fragment_data["metadata"]["classification"] = fragment.classification
            
            # For images - reference to image file
            # ImageFragment stores image in value, not in image
            fragment_image = None
            if hasattr(fragment, 'image') and fragment.image:
                fragment_image = fragment.image
            elif hasattr(fragment, 'value') and hasattr(fragment.value, 'save'):  # PIL Image check
                fragment_image = fragment.value
            
            if save_images and fragment_image:
                fragment_data["image_file"] = f"fragment_images/{fragment_id}.png"
                if hasattr(fragment_image, 'size'):
                    fragment_data["metadata"]["dimensions"] = list(fragment_image.size)
            
            fragments_data.append(fragment_data)
        
        return {"fragments": fragments_data}
    
    def serialize_structure(self, document: Document) -> Dict[str, Any]:
        """Serialize document structure and hierarchy."""
        
        fragments = document.fragments()
        
        # Build reading order (simple by index for now)
        reading_order = [f"fragment_{i+1:03d}" for i in range(len(fragments))]
        
        # Group by pages
        page_structure = {}
        for i, fragment in enumerate(fragments):
            page = getattr(fragment, 'page', 1) or 1
            page_key = str(page)
            if page_key not in page_structure:
                page_structure[page_key] = []
            page_structure[page_key].append(f"fragment_{i+1:03d}")
        
        # Basic hierarchy (can be extended in future)
        hierarchy = {
            "root": {
                "fragment_id": None,
                "children": []
            }
        }
        
        # Simple linear hierarchy by levels
        current_level_stack = [hierarchy["root"]]
        
        for i, fragment in enumerate(fragments):
            fragment_id = f"fragment_{i+1:03d}"
            
            # Use same logic as in serialize_fragments
            style = getattr(fragment, 'style', {}) or {}
            level = getattr(fragment, 'level', None) or style.get('level')
            
            # For headers, determine default level
            fragment_type = fragment.__class__.__name__.lower()
            if level is None and 'header' in fragment_type:
                if 'title' in fragment_type:
                    level = 1  # TitleFragment = level 1
                else:
                    level = 2  # HeaderFragment = level 2
            
            node = {
                "fragment_id": fragment_id,
                "level": level,
                "children": []
            }
            
            if level is not None and level > 0:
                # Find suitable parent level
                while len(current_level_stack) > level:
                    current_level_stack.pop()
                
                # Add to current parent
                if current_level_stack:
                    current_level_stack[-1]["children"].append(node)
                    current_level_stack.append(node)
                else:
                    hierarchy["root"]["children"].append(node)
                    current_level_stack = [hierarchy["root"], node]
            else:
                # Fragment without level - add to last header or root
                if len(current_level_stack) > 1:
                    # Add to last header
                    current_level_stack[-1]["children"].append(node)
                else:
                    # Add to root
                    hierarchy["root"]["children"].append(node)
        
        return {
            "hierarchy": hierarchy,
            "reading_order": reading_order,
            "page_structure": page_structure
        }
    
    def save_json(self, data: Dict[str, Any], file_path: Path) -> None:
        """Save data to JSON file."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
