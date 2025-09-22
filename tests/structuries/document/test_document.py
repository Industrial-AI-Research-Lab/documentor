from typing import Any

import pytest

from documentor.data.structures.document.base import Document
from documentor.data.structures.document.text import TextDocument
from documentor.data.structures.fragment.text import TextFragment


@pytest.mark.parametrize(
    "doc_cls, kwargs, values",
    [
        (TextDocument, {"lines_count": 0}, [""]),
        (TextDocument, {"lines_count": 1}, ["a"]),
        (TextDocument, {"lines_count": 3}, ["a", "b", "c"]),
    ],
)
def test_document_fragments_and_iteration(doc_cls: type[Document], kwargs: dict[str, Any], values: list[str]):
    fragments = [TextFragment(v) for v in values]
    doc = doc_cls(fragments=fragments, **kwargs)

    # fragments() returns the same sequence
    assert [str(f) for f in doc.fragments()] == values

    # iter_fragments yields the same items lazily
    assert [str(f) for f in doc.iter_fragments()] == values


def test_documents_are_independent():
    doc1 = TextDocument(lines_count=1, fragments=[TextFragment("a")])
    doc2 = TextDocument(lines_count=2, fragments=[TextFragment("b"), TextFragment("c")])

    # Ensure no shared state between instances
    assert [str(f) for f in doc1.fragments()] == ["a"]
    assert [str(f) for f in doc2.fragments()] == ["b", "c"]

    # Mutating one should not affect the other
    doc1.fragments().append(TextFragment("z"))
    assert [str(f) for f in doc1.fragments()] == ["a", "z"]
    assert [str(f) for f in doc2.fragments()] == ["b", "c"]
