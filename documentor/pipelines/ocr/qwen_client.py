"""Client for working with Qwen2.5-VL model."""

from typing import Any, Dict, List, Optional

from PIL import Image

from .api_client import APIConfig, BaseAPIClient
from .prompts import (
    QWEN_WORD_DETECTION_SYSTEM_PROMPT,
    QWEN_WORD_DETECTION_USER_PROMPT,
    QWEN_WORD_RECOGNITION_SYSTEM_PROMPT,
    QWEN_WORD_RECOGNITION_USER_PROMPT,
)


class QwenClient(BaseAPIClient):
    """Client for working with Qwen2.5-VL model for OCR recognition."""
    
    def __init__(self, config: APIConfig):
        super().__init__(config)
    
    def _build_word_detection_prompt(self) -> str:
        """Create prompt for word detection."""
        return QWEN_WORD_DETECTION_USER_PROMPT
    
    def _build_word_recognition_prompt(self) -> str:
        """Create prompt for word recognition."""
        return QWEN_WORD_RECOGNITION_USER_PROMPT
    
    def _create_word_detection_messages(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Create messages for word detection."""
        processed_image = self._resize_image_if_needed(image)
        width, height = processed_image.size
        
        system_prompt = QWEN_WORD_DETECTION_SYSTEM_PROMPT
        user_prompt = self._build_word_detection_prompt()
        
        return self._build_messages(processed_image, system_prompt, user_prompt)
    
    def _create_word_recognition_messages(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Create messages for word recognition."""
        processed_image = self._resize_image_if_needed(image)
        width, height = processed_image.size
        
        system_prompt = QWEN_WORD_RECOGNITION_SYSTEM_PROMPT
        user_prompt = self._build_word_recognition_prompt()
        
        return self._build_messages(processed_image, system_prompt, user_prompt)
    
    def _build_messages(self, image: Image.Image, system_prompt: str, user_prompt: str) -> List[Dict[str, Any]]:
        """Create messages with image."""
        image_base64 = self._image_to_base64(image)
        return [
            {"role": "system", "content": system_prompt},
            {
                "role": "user", 
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_base64
                        }
                    },
                    {"type": "text", "text": user_prompt}
                ]
            }
        ]
    
    def detect_words(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Detect words in image and return word detection results."""
        messages = self._create_word_detection_messages(image)
        
        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        
        content = response.choices[0].message.content
        return self._parse_word_detection_response(content)
    
    def recognize_text(self, image: Image.Image) -> str:
        """Recognize text in image and return plain text."""
        messages = self._create_word_recognition_messages(image)
        
        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        
        content = response.choices[0].message.content
        return content.strip()
    
    def _parse_word_detection_response(self, content: str) -> List[Dict[str, Any]]:
        """Parse word detection response and return structured data."""
        import json
        
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
            return []
        except json.JSONDecodeError:
            return []
    
    def process_image(self, image: Image.Image) -> str:
        """Process image and return recognized text (implements abstract method)."""
        return self.recognize_text(image)
