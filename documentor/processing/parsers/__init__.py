"""Document parser system without LangChain dependencies."""

from .txt_parser import TxtParser
from .image_parser import ImageParser
from .pdf_parser import PdfParser
from .registry import ParserRegistry

__all__ = [
    "TxtParser",
    "ImageParser", 
    "PdfParser",
    "ParserRegistry",
]
