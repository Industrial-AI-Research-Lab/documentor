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

    Attributes:
        value (PIL.Image.Image): The image content of the formula.
        format (str): Image format used for serialization.
        encoding (str): Text encoding used for base64 conversion.
        description (str): Fragment type description for LLMs.
        need_to_recognize (bool): Indicates if OCR/recognition is required for this fragment.
    """
    description: str = FORMULA
    is_processed: bool = False


@dataclass
class LatexFormulaFragment(TextFragment):
    """
    Implementation for formula fragments that have a LaTeX value.

    Attributes:
        value (str): LaTeX source string of the formula.
        description (str): Fragment type description for LLMs.
        source (PIL.Image.Image | None): Optional original image of the formula.
    """
    description: str = FORMULA
    source: Image | None = None
