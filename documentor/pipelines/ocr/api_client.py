"""API клиент для общения с моделями через OpenAI-совместимый API."""

import base64
import io
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import openai
from PIL import Image


@dataclass
class APIConfig:
    """Конфигурация для API клиента."""
    base_url: str
    api_key: str
    model_name: str = "/model"
    temperature: float = 0.1
    max_tokens: int = 4096
    timeout: int = 30


class BaseAPIClient(ABC):
    """Базовый класс для API клиентов."""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.client = openai.OpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
            timeout=config.timeout
        )
    
    def _image_to_base64(self, image: Image.Image) -> str:
        """Конвертирует PIL изображение в base64 строку."""
        if hasattr(image, 'format') and image.format:
            format_type = image.format.upper()
        else:
            format_type = 'PNG'
        
        # Нормализация формата для корректного MIME типа
        if format_type in ['JPG', 'JPEG']:
            format_type = 'JPEG'
            mime_type = 'jpeg'
        elif format_type == 'PNG':
            mime_type = 'png'
        elif format_type in ['GIF', 'WEBP']:
            mime_type = format_type.lower()
        else:
            format_type = 'PNG'
            mime_type = 'png'
        
        buffer = io.BytesIO()
        image.save(buffer, format=format_type)
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/{mime_type};base64,{img_str}"
    
    def _resize_image_if_needed(self, image: Image.Image, max_size: int = 2048) -> Image.Image:
        """Изменяет размер изображения если оно слишком большое."""
        width, height = image.size
        if max(width, height) > max_size:
            ratio = max_size / max(width, height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return image
    
    @abstractmethod
    def process_image(self, image: Image.Image) -> Any:
        """Обрабатывает изображение и возвращает результат."""
        pass