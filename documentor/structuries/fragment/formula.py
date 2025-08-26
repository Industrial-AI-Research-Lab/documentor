"""
Formula fragments.

Contains:
- ImageFormulaFragment: formula represented as an image.
- LatexFormulaFragment: formula represented as LaTeX string (with optional source image reference).
"""
from dataclasses import dataclass

from PIL.Image import Image

from .image import ImageFragment
from .text import TextFragment
from .description import FORMULA


@dataclass
class ImageFormulaFragment(ImageFragment):
    """
    Implementation for formula fragments that have an image value.
    """
    description: str = FORMULA


@dataclass
class LatexFormulaFragment(TextFragment):
    """
    Implementation for formula fragments that have a LaTeX value.
    Attributes:
        source (Image): Optional original image of the formula.
    """
    description: str = FORMULA
    source: Image | None = None
