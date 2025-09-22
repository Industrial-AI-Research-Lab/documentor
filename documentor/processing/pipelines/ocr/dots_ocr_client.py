"""Client for working with dots.ocr model."""

from typing import Any, Dict, List, Optional, Tuple
import json

from PIL import Image

from .api_client import APIConfig, BaseAPIClient
from .prompts import DOTS_LAYOUT_PROMPT, DOTS_SYSTEM_PROMPT


class DotsOCRClient(BaseAPIClient):
    """Client for working with dots.ocr model for layout detection."""
    
    def __init__(self, config: APIConfig):
        super().__init__(config)
        self.layout_categories = {
            'Caption', 'Footnote', 'Formula', 'List-item', 
            'Page-footer', 'Page-header', 'Picture', 
            'Section-header', 'Table', 'Text', 'Title'
        }
    
    def _build_layout_prompt(self, image_width: int, image_height: int) -> str:
        """Create prompt for layout analysis."""
        return DOTS_LAYOUT_PROMPT
    
    def _create_messages(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Create messages for the model."""
        processed_image = self._resize_image_if_needed(image)
        width, height = processed_image.size
        
        system_prompt = DOTS_SYSTEM_PROMPT.format(width=width, height=height)
        user_prompt = self._build_layout_prompt(width, height)
        
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
    
    def process_image(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Process image and return list of layout elements."""
        messages = self._create_messages(image)
        
        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        
        content = response.choices[0].message.content
        return self._parse_layout_response(content)
    
    def _parse_layout_response(self, content: str) -> List[Dict[str, Any]]:
        """Parse model response and return structured data."""
        try:
            # Try to parse JSON
            data = json.loads(content)
            
            # If it's a list of elements
            if isinstance(data, list):
                elements = data
            # If it's an object with elements array
            elif isinstance(data, dict) and 'elements' in data:
                elements = data['elements']
            else:
                elements = [data]
            
            result = []
            for element in elements:
                if not isinstance(element, dict):
                    continue
                
                # Check required fields
                if 'bbox' not in element or 'category' not in element:
                    continue
                
                bbox = element['bbox']
                category = element['category']
                
                # Validate bbox
                if not isinstance(bbox, list) or len(bbox) != 4:
                    continue
                
                # Validate category
                if category not in self.layout_categories:
                    continue
                
                # Convert bbox to tuple
                try:
                    bbox_tuple = tuple(int(coord) for coord in bbox)
                except (ValueError, TypeError):
                    continue
                
                result.append({
                    'type': category,
                    'bbox': bbox_tuple,
                    'confidence': element.get('confidence', 1.0)
                })
            
            return result
            
        except json.JSONDecodeError:
            # If JSON doesn't parse, try to extract data from text
            return self._parse_text_response(content)
    
    def _parse_text_response(self, content: str) -> List[Dict[str, Any]]:
        """Parse text response (fallback)."""
        elements = []
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or '|' not in line:
                continue
            
            try:
                parts = line.split('|')
                if len(parts) != 2:
                    continue
                
                element_type = parts[0].strip()
                coords_str = parts[1].strip()
                
                if element_type not in self.layout_categories:
                    continue
                
                coords = coords_str.split(',')
                if len(coords) != 4:
                    continue
                
                x1, y1, x2, y2 = map(int, coords)
                
                elements.append({
                    'type': element_type,
                    'bbox': (x1, y1, x2, y2),
                    'confidence': 1.0
                })
                
            except (ValueError, IndexError):
                continue
        
        return elements