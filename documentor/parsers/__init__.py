"""Collection of built-in document parsers."""

from .image import ImageParser
from .pdf import PdfParser

__all__ = ["ImageParser", "PdfParser"]
