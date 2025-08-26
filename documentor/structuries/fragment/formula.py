from PIL.Image import Image

from structuries.fragment import ImageFragment, TextFragment
from structuries.fragment.description import FORMULA


class ImageFormulaFragment(ImageFragment):
    """
    Implementation for formula fragments that have an image value.
    """
    description: str = FORMULA


class LatexFormulaFragment(TextFragment):
    """
    Implementation for formula fragments that have a latex value.
    """
    description: str = FORMULA
    source: Image