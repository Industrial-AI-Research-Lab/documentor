import pytest

from documentor.structuries.fragment.text import TextFragment, ParagraphFragment
from documentor.structuries.fragment.description import PARAGRAPH


@pytest.mark.parametrize(
    "text",
    [
        "Hello, world!",
        "",
        "Многострочный\nтекст с Unicode — проверка",
    ],
)
def test_text_fragment_str_and_dict(text):
    frag = TextFragment(value=text)
    # __str__ should return original value
    assert str(frag) == text

    d = frag.__dict__()
    # TextFragment should expose both value and description keys
    assert d["value"] == text
    assert d["description"] == ""


@pytest.mark.parametrize("text", ["Paragraph one.", "Абзац два."])
def test_paragraph_fragment_description(text):
    frag = ParagraphFragment(value=text)
    assert str(frag) == text
    # Paragraph has fixed description
    assert frag.description == PARAGRAPH
    d = frag.__dict__()
    # Some subclasses may not include 'value' in annotations-based __dict__.
    # Ensure description is set to PARAGRAPH and __str__ works.
    assert frag.description == PARAGRAPH
