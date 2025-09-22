"""OCR pipeline utilities."""

from .api_client import APIConfig, BaseAPIClient
from .config import OCRPipelineConfig
from .dots_ocr_client import DotsOCRClient
from .qwen_client import QwenClient
from .detector import DotsBlockDetector
from .recognizer import QwenBlockRecognizer
from .category_mapping import DOTS_CATEGORY_MAPPING
from .pdf_processor import PDFProcessor
from .prompts import (
    DOTS_LAYOUT_PROMPT,
    DOTS_SYSTEM_PROMPT,
    QWEN_WORD_DETECTION_SYSTEM_PROMPT,
    QWEN_WORD_DETECTION_USER_PROMPT,
    QWEN_WORD_RECOGNITION_SYSTEM_PROMPT,
    QWEN_WORD_RECOGNITION_USER_PROMPT,
)
from .interfaces import (
    Block,
    BlockDetector,
    BlockClassifier,
    OrderRestorer,
    BlockRecognizer,
)
from .pipeline import ScanPipeline

__all__ = [
    "APIConfig",
    "BaseAPIClient",
    "OCRPipelineConfig",
    "DotsOCRClient",
    "QwenClient",
    "DotsBlockDetector",
    "QwenBlockRecognizer",
    "DOTS_CATEGORY_MAPPING",
    "PDFProcessor",
    "DOTS_LAYOUT_PROMPT",
    "DOTS_SYSTEM_PROMPT",
    "QWEN_WORD_DETECTION_SYSTEM_PROMPT",
    "QWEN_WORD_DETECTION_USER_PROMPT",
    "QWEN_WORD_RECOGNITION_SYSTEM_PROMPT",
    "QWEN_WORD_RECOGNITION_USER_PROMPT",
    "Block",
    "BlockDetector",
    "BlockClassifier",
    "OrderRestorer",
    "BlockRecognizer",
    "ScanPipeline",
]