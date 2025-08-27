import pytest
import pandas as pd

from structuries.document.base import Document
from structuries.document.text import TextDocument
from structuries.document.sheet import SheetDocument
from structuries.document.doc import DocDocument
from structuries.fragment.text import TextFragment


@pytest.mark.parametrize(
    "doc_cls, values",
    [
        (TextDocument, []),
        (TextDocument, ["a"]),
        (TextDocument, ["a", "b", "c"]),
        (SheetDocument, ["row1"]),
        (DocDocument, ["x", "y"]),
    ],
)
def test_document_fragments_and_iteration(doc_cls: type[Document], values: list[str]):
    fragments = [TextFragment(v) for v in values]
    doc = doc_cls(fragments)

    # fragments() returns the same sequence
    assert [str(f) for f in doc.fragments()] == values

    # iter_fragments yields the same items lazily
    assert [str(f) for f in doc.iter_fragments()] == values


def test_documents_are_independent():
    doc1 = TextDocument([TextFragment("a")])
    doc2 = TextDocument([TextFragment("b"), TextFragment("c")])

    # Ensure no shared state between instances
    assert [str(f) for f in doc1.fragments()] == ["a"]
    assert [str(f) for f in doc2.fragments()] == ["b", "c"]

    # Mutating one should not affect the other
    doc1.fragments().append(TextFragment("z"))
    assert [str(f) for f in doc1.fragments()] == ["a", "z"]
    assert [str(f) for f in doc2.fragments()] == ["b", "c"]
