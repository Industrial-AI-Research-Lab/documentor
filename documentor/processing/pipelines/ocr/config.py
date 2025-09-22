"""Configuration for OCR pipeline."""

from dataclasses import dataclass
from typing import Optional

from .api_client import APIConfig
from documentor.core.env_config import env


@dataclass
class OCRPipelineConfig:
    """Configuration for OCR pipeline."""
    
    # Configuration for dots.ocr
    dots_ocr_config: APIConfig
    
    # Configuration for Qwen2.5-VL
    qwen_config: APIConfig
    
    # General settings
    max_image_size: int = 2048
    min_confidence: float = 0.5
    
    @classmethod
    def create_default(cls) -> 'OCRPipelineConfig':
        """Create default configuration."""
        # Validate required environment variables
        required_vars = [
            "DOTS_OCR_BASE_URL", "DOTS_OCR_API_KEY", "DOTS_OCR_MODEL_NAME",
            "QWEN_BASE_URL", "QWEN_API_KEY", "QWEN_MODEL_NAME"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not env.get_str(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                f"Please set them in your .env file or environment."
            )
        
        dots_ocr_config = APIConfig(
            base_url=env.get_str("DOTS_OCR_BASE_URL"),
            api_key=env.get_str("DOTS_OCR_API_KEY"),
            model_name=env.get_str("DOTS_OCR_MODEL_NAME"),
            temperature=env.get_float("DOTS_OCR_TEMPERATURE", 0.1),
            max_tokens=env.get_int("DOTS_OCR_MAX_TOKENS", 4096),
            timeout=env.get_int("DOTS_OCR_TIMEOUT", 30)
        )
        
        qwen_config = APIConfig(
            base_url=env.get_str("QWEN_BASE_URL"),
            api_key=env.get_str("QWEN_API_KEY"),
            model_name=env.get_str("QWEN_MODEL_NAME"),
            temperature=env.get_float("QWEN_TEMPERATURE", 0.1),
            max_tokens=env.get_int("QWEN_MAX_TOKENS", 4096),
            timeout=env.get_int("QWEN_TIMEOUT", 30)
        )
        
        return cls(
            dots_ocr_config=dots_ocr_config,
            qwen_config=qwen_config,
            max_image_size=env.get_int("OCR_MAX_IMAGE_SIZE", 2048),
            min_confidence=env.get_float("OCR_MIN_CONFIDENCE", 0.5)
        )