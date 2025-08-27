from typing import Any

from langchain_core.documents.base import Blob


class Metadata:
    name: str | None = None
    extension: str | None = None
    source: Blob | None = None
    params: dict[str, Any] = {}

    def __init__(
            self,
            name: str | None = None,
            extension: str | None = None,
            source: Blob | None = None,
            **kwargs,
    ):
        self.name = name
        self.extension = extension
        self.source = source
        self.params = kwargs
