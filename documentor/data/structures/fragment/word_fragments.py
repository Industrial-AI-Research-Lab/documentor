"""
Word-specific fragments for DOC/DOCX document processing.

Contains fragments specific to Microsoft Word documents that extend
the base fragment types with Word-specific functionality.
"""

from dataclasses import dataclass
from typing import Optional

try:
    from overrides import overrides
except Exception:
    # Fallback no-op decorator if `overrides` is not installed
    def overrides(method=None, *args, **kwargs):
        if callable(method):
            return method
        def decorator(func):
            return func
        return decorator

from .base import Fragment
from .text import TextFragment


@dataclass 
class HyperlinkFragment(TextFragment):
    """
    Hyperlink fragment for clickable links in Word documents.
    
    Attributes:
        value (str): Display text of the link
        url (str): Target URL
        tooltip (str): Optional tooltip text
    """
    url: Optional[str] = None
    tooltip: Optional[str] = None
    
    @classmethod
    def description(cls) -> str:
        return "HYPERLINK"
    
    @overrides
    def __str__(self) -> str:
        if self.url:
            return f"{self.value} ({self.url})"
        return self.value


@dataclass
class StyleFragment(TextFragment):
    """
    Text fragment with rich formatting information from Word documents.
    
    Attributes:
        value (str): Text content
        font_family (str): Font family name
        font_size (int): Font size in points
        is_bold (bool): Bold formatting
        is_italic (bool): Italic formatting
        is_underline (bool): Underline formatting
        text_color (str): Text color (hex format)
        background_color (str): Background color (hex format)
        alignment (str): Text alignment (left, center, right, justify)
    """
    font_family: Optional[str] = None
    font_size: Optional[int] = None
    is_bold: bool = False
    is_italic: bool = False
    is_underline: bool = False
    text_color: Optional[str] = None
    background_color: Optional[str] = None
    alignment: Optional[str] = None
    
    @classmethod
    def description(cls) -> str:
        return "STYLED_TEXT"
    
    @overrides
    def __str__(self) -> str:
        return self.value


@dataclass
class CommentFragment(Fragment):
    """
    Comment fragment for document comments and annotations in Word documents.
    
    Attributes:
        value (str): Comment text
        author (str): Comment author
        date (str): Comment date
        comment_id (str): Comment identifier
        target_text (str): Text that comment refers to
    """
    value: str
    author: Optional[str] = None
    date: Optional[str] = None
    comment_id: Optional[str] = None
    target_text: Optional[str] = None
    
    @classmethod
    def description(cls) -> str:
        return "COMMENT"
    
    @overrides
    def __str__(self) -> str:
        author_part = f" by {self.author}" if self.author else ""
        return f"[Comment{author_part}]: {self.value}"


@dataclass
class BreakFragment(Fragment):
    """
    Break fragment for page breaks, section breaks, etc. in Word documents.
    
    Attributes:
        value (str): Type of break
        break_type (str): Specific break type (page, section, column)
    """
    value: str = "BREAK"
    break_type: Optional[str] = None
    
    @classmethod
    def description(cls) -> str:
        return "BREAK"
    
    @overrides
    def __str__(self) -> str:
        if self.break_type:
            return f"[{self.break_type.upper()} BREAK]"
        return "[BREAK]"
