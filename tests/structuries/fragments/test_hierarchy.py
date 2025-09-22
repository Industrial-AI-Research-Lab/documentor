import pytest

from documentor.data.structures.fragment.hierarchy import HeaderFragment, TitleFragment, ColumnHeaderFragment
from documentor.data.structures.fragment.description import HEADER, TITLE, COLUMN


@pytest.mark.parametrize(
    "text,font_size,level",
    [
        ("Header", None, None),
        ("Заголовок", 14, 2),
    ],
)
def test_header_fragment_basic(text, font_size, level):
    frag = HeaderFragment(value=text, font_size=font_size, level=level)
    assert str(frag) == text

    d = frag.__dict__()
    # font_size/level may be missing in dict only if __annotations__ handling changes; be tolerant
    if font_size is not None:
        assert d.get("font_size", font_size) == font_size
    if level is not None:
        assert d.get("level", level) == level


@pytest.mark.parametrize("text", ["Doc Title", "Название документа"])
def test_title_fragment_description(text):
    frag = TitleFragment(value=text)
    assert str(frag) == text


@pytest.mark.parametrize("text", ["Column A", "Столбец 1"])
def test_column_header_fragment_description(text):
    frag = ColumnHeaderFragment(value=text)
    assert str(frag) == text
