"""PDF parser that relies on the OCR scan pipeline."""

from __future__ import annotations

from typing import Iterable, Any, Callable, Iterator

from documentor.parsers.base import BaseBlobParser
from documentor.parsers.extensions import DocExtension
from documentor.parsers.config import ParsingSchema
from documentor.structuries.document import Document, Metadata
from documentor.structuries.fragment.base import Fragment
from documentor.pipelines.ocr import ScanPipeline
from langchain_core.documents.base import Blob

try:  # pragma: no cover - optional dependency
    from pdf2image import convert_from_bytes  # type: ignore
except Exception:  # pragma: no cover
    convert_from_bytes = None


class PdfParser(BaseBlobParser):
    """Parse PDF bytes using a :class:`~documentor.pipelines.ocr.ScanPipeline`."""

    _extensions = {DocExtension.pdf}
    _available_parsing_schemas = {ParsingSchema.full}

    def __init__(
        self,
        pipeline: ScanPipeline,
        pdf_to_images: Callable[[bytes], Iterable[Any]] | None = None,
        **kwargs,
    ) -> None:
        self.pipeline = pipeline
        self._pdf_to_images = pdf_to_images or convert_from_bytes
        super().__init__(**kwargs)

    def _create_document(
        self,
        fragments: list[Fragment],
        page_number: int,
        file_name: str | None,
        source: Blob | None,
        file_type: str | None,
    ) -> Document:
        metadata = Metadata(name=file_name, extension=file_type, source=source, page=page_number)
        return Document(fragments=fragments, metadata=metadata)

    def _build_document(self, fragments: list[Fragment], page_number: int, blob: Blob) -> Document:
        file_name = blob.path.name if blob.path else None
        file_type = blob.path.suffix if blob.path else None
        return self._create_document(fragments, page_number, file_name, blob, file_type)

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        if self._pdf_to_images is None:
            raise ImportError("pdf2image is required to parse PDF files")
        pdf_bytes = blob.as_bytes()
        for page_number, page_image in enumerate(self._pdf_to_images(pdf_bytes)):
            fragments = list(self.pipeline(page_image))
            yield self._build_document(fragments, page_number, blob)
