from __future__ import annotations

"""Interfaces for OCR pipeline stages.

These minimal ABCs define the contract for each stage of an OCR pipeline.
Custom implementations can be provided to plug into the :class:`ScanPipeline`.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Any

from documentor.structuries.fragment.base import Fragment


@dataclass
class Block:
    """Container representing a detected block in an image.

    The block may represent a line of text, table, image or any other
    structural element detected on a page.  The container keeps only the
    minimum information required for the subsequent stages of the pipeline
    and deliberately avoids tying to any specific OCR library.

    Attributes:
        image:    Cropped image data for the block.  Type is intentionally
                   loose to allow use of any imaging library (e.g. PIL, numpy).
        bbox:     Optional bounding box in (x1, y1, x2, y2) coordinates.
        category: Optional classification label supplied by
                  :class:`BlockClassifier`.
        order:    Optional index representing the reading order.
    """

    image: Any
    bbox: tuple[int, int, int, int] | None = None
    category: str | None = None
    order: int | None = None


class BlockDetector(ABC):
    """Stage responsible for locating blocks on a page image."""

    @abstractmethod
    def detect(self, image: Any) -> Iterable[Block]:
        """Detect blocks on a raw page image."""
        raise NotImplementedError


class BlockClassifier(ABC):
    """Stage responsible for assigning semantic labels to blocks."""

    @abstractmethod
    def classify(self, blocks: Iterable[Block]) -> Iterable[Block]:
        """Annotate blocks with semantic categories."""
        raise NotImplementedError


class OrderRestorer(ABC):
    """Stage that establishes reading order for blocks."""

    @abstractmethod
    def restore(self, blocks: Iterable[Block]) -> Iterable[Block]:
        """Return blocks in the desired reading order."""
        raise NotImplementedError


class BlockRecognizer(ABC):
    """Stage that converts blocks into :class:`Fragment` objects."""

    @abstractmethod
    def recognize(self, blocks: Iterable[Block]) -> Iterable[Fragment]:
        """Yield :class:`Fragment` objects with recognized content."""
        raise NotImplementedError
