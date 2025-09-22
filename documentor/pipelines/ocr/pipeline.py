from __future__ import annotations

"""Orchestration of OCR pipeline stages."""

from typing import Iterable, Iterator, Any

from documentor.structuries.fragment.base import Fragment

from .interfaces import (
    BlockDetector,
    BlockClassifier,
    OrderRestorer,
    BlockRecognizer,
)


class ScanPipeline:
    """Run a sequence of OCR stages to produce :class:`Fragment` objects.

    The pipeline is deliberately lightweight.  Every stage is pluggable and
    may be swapped for custom implementations, e.g. a different detector or a
    recognizer using another LLM prompt.
    """

    def __init__(
        self,
        detector: BlockDetector,
        classifier: BlockClassifier | None = None,
        order_restorer: OrderRestorer | None = None,
        recognizer: BlockRecognizer | None = None,
    ) -> None:
        self.detector = detector
        self.classifier = classifier
        self.order_restorer = order_restorer
        self.recognizer = recognizer

    def process(self, image: Any) -> Iterator[Fragment]:
        """Process a page image through all configured stages."""

        blocks: Iterable = self.detector.detect(image)

        if self.classifier is not None:
            blocks = self.classifier.classify(blocks)

        if self.order_restorer is not None:
            blocks = self.order_restorer.restore(blocks)

        if self.recognizer is None:
            return iter(())

        yield from self.recognizer.recognize(blocks)

    # Allow the pipeline instance to be called directly
    __call__ = process
