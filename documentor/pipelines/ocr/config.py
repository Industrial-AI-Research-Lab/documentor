"""Конфигурация для OCR пайплайна."""

from dataclasses import dataclass
from typing import Optional

from .api_client import APIConfig


@dataclass
class OCRPipelineConfig:
    """Конфигурация для OCR пайплайна."""
    
    # Конфигурация для dots.ocr
    dots_ocr_config: APIConfig
    
    # Конфигурация для Qwen2.5-VL
    qwen_config: APIConfig
    
    # Общие настройки
    max_image_size: int = 2048
    min_confidence: float = 0.5
    
    @classmethod
    def create_default(cls) -> 'OCRPipelineConfig':
        """Создает конфигурацию по умолчанию."""
        dots_ocr_config = APIConfig(
            base_url="http://10.32.2.11:8069/v1",
            api_key="security-token-abc123",
            model_name="/model",
            temperature=0.1,
            max_tokens=4096
        )
        
        qwen_config = APIConfig(
            base_url="http://10.32.2.11:8069/v1",
            api_key="security-token-abc123",
            model_name="/model",
            temperature=0.1,
            max_tokens=4096
        )
        
        return cls(
            dots_ocr_config=dots_ocr_config,
            qwen_config=qwen_config
        )