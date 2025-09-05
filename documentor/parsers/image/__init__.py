"""Image parser powered by the OCR scan pipeline."""

from __future__ import annotations

from typing import Iterator
from io import BytesIO

try:  # pragma: no cover - optional dependency
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None

from documentor.parsers.base import BaseBlobParser
from documentor.parsers.extensions import DocExtension
from documentor.parsers.config import ParsingSchema
from documentor.structuries.document import Document, Metadata
from documentor.structuries.fragment.base import Fragment
from documentor.pipelines.ocr import ScanPipeline
from langchain_core.documents.base import Blob


class ImageParser(BaseBlobParser):
    """Parse images using a :class:`~documentor.pipelines.ocr.ScanPipeline`."""

    _extensions = {DocExtension.jpg, DocExtension.jpeg, DocExtension.png}
    _available_parsing_schemas = {ParsingSchema.full}

    def __init__(self, pipeline: ScanPipeline, **kwargs) -> None:
        self.pipeline = pipeline
        super().__init__(**kwargs)

    def _create_document(
        self,
        fragments: list[Fragment],
        line_number: int,
        file_name: str | None,
        source: Blob | None,
        file_type: str | None,
    ) -> Document:
        metadata = Metadata(name=file_name, extension=file_type, source=source)
        return Document(fragments=fragments, metadata=metadata)

    def _build_document(self, fragments: list[Fragment], line_number: int, blob: Blob) -> Document:
        file_name = blob.path.name if blob.path else None
        file_type = blob.path.suffix if blob.path else None
        return self._create_document(fragments, line_number, file_name, blob, file_type)

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        if Image is None:
            raise ImportError("Pillow is required to parse image files")
        image = Image.open(BytesIO(blob.as_bytes()))
        fragments = list(self.pipeline(image))
        yield self._build_document(fragments, 0, blob)
