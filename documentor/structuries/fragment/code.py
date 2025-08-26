"""
Code listing fragment.

Contains:
- ListingFragment: represents code or log listing as plain text.
"""
from .description import LISTING
from .text import TextFragment


class ListingFragment(TextFragment):
    """
    Implementation for listing text fragments with only a str value.
    """
    description: str = LISTING
