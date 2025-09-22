"""BlockDetector implementation for dots.ocr."""

from typing import Iterable, Any

from PIL import Image

from .interfaces import Block, BlockDetector
from .dots_ocr_client import DotsOCRClient
import logging

logger = logging.getLogger(__name__)


class DotsBlockDetector(BlockDetector):
    """BlockDetector using dots.ocr for layout detection."""
    
    def __init__(self, dots_client: DotsOCRClient):
        self.dots_client = dots_client
    
    def detect(self, image: Any) -> Iterable[Block]:
        """Detect blocks on a raw page image."""
        if not isinstance(image, Image.Image):
            raise ValueError("Image must be a PIL Image")
        
        # Get layout elements from dots.ocr
        layout_elements = self.dots_client.process_image(image)
        
        # Convert to Block objects
        blocks = []
        for i, element in enumerate(layout_elements):
            # Crop image by bbox
            bbox = element['bbox']
            cropped_image = image.crop(bbox)
            
            # Scale image if it's too small for Qwen
            cropped_image = self._ensure_minimum_size(cropped_image, min_size=32)
            
            block = Block(
                image=cropped_image,
                bbox=bbox,
                category=element['type'],
                order=i,  # Simple order
                confidence=element['confidence'],
                layout_hints={
                    'source': 'dots.ocr',
                    'original_category': element['type'],
                    'original_size': bbox  # Save original size
                }
            )
            blocks.append(block)
        
        return blocks
    
    def _ensure_minimum_size(self, image: Image.Image, min_size: int = 32) -> Image.Image:
        """
        Increase image to minimum size if needed.
        
        Qwen2.5-VL can fail on very small images.
        
        Args:
            image: PIL image
            min_size: Minimum size in pixels
            
        Returns:
            Image.Image: Image with size not less than min_size
        """
        width, height = image.size
        
        # If image is already large enough
        if width >= min_size and height >= min_size:
            return image
        
        # Calculate new size preserving aspect ratio
        scale_factor = max(min_size / width, min_size / height)
        new_width = max(int(width * scale_factor), min_size)
        new_height = max(int(height * scale_factor), min_size)
        
        # Scale image with quality resampling
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        logger.info(f"Image enlarged: {width}x{height} -> {new_width}x{new_height}")
        
        return resized_image
