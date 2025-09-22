"""BlockRecognizer implementation for dots.ocr."""

from typing import Iterable, Any

from PIL import Image

from documentor.data.structures.fragment.base import Fragment
from .interfaces import Block, BlockRecognizer
from .qwen_client import QwenClient
from .category_mapping import DOTS_CATEGORY_MAPPING


class QwenBlockRecognizer(BlockRecognizer):
    """BlockRecognizer using Qwen2.5-VL for OCR recognition."""
    
    def __init__(self, qwen_client: QwenClient | None = None):
        self.qwen_client = qwen_client
    
    def recognize(self, blocks: Iterable[Block]) -> Iterable[Fragment]:
        """Yield Fragment objects with recognized content."""
        for block in blocks:
            # Handle Picture blocks separately - create ImageFragment without OCR
            if block.category == 'Picture':
                fragment_class = DOTS_CATEGORY_MAPPING.get(block.category)
                if fragment_class and block.image:
                    # Create ImageFragment with the actual image
                    fragment = fragment_class(
                        value=block.image,  # PIL Image object
                        bbox=block.bbox,
                        style={
                            'confidence': block.confidence,
                            'bbox': block.bbox,
                            'source': 'dots.ocr'
                        }
                    )
                    yield fragment
                continue
            
            # Use Qwen2.5-VL for OCR recognition for text blocks
            if not self.qwen_client:
                continue
                
            try:
                text = self.qwen_client.recognize_text(block.image)
            except Exception:
                # If Qwen fails, skip this block
                continue
            
            if not text or not text.strip():
                continue
            
            # Create corresponding Fragment
            fragment_class = DOTS_CATEGORY_MAPPING.get(block.category)
            if not fragment_class:
                continue
            
            # Create Fragment with text from Qwen2.5-VL
            fragment = fragment_class(
                value=text,
                style={
                    'confidence': block.confidence,
                    'bbox': block.bbox,
                    'source': 'qwen2.5-vl'
                }
            )
            
            yield fragment
