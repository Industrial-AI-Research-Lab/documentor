"""BlockDetector implementation for dots.ocr."""

from typing import Iterable, Any

from PIL import Image

from .interfaces import Block, BlockDetector
from .dots_ocr_client import DotsOCRClient


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
            
            block = Block(
                image=cropped_image,
                bbox=bbox,
                category=element['type'],
                order=i,  # Simple order
                confidence=element['confidence'],
                layout_hints={
                    'source': 'dots.ocr',
                    'original_category': element['type']
                }
            )
            blocks.append(block)
        
        return blocks
