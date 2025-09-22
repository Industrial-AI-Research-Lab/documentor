import pytest

from documentor.data.structures.structure import DocumentStructure, StructureNode
from documentor.data.structures.fragment.hierarchy import HeaderFragment
from documentor.data.structures.fragment.text import TextFragment


@pytest.fixture
def sample_structure():
    """Create a small hierarchy for testing."""
    a1 = TextFragment("A1", id="a1")
    a2 = TextFragment("A2", id="a2")
    b1 = TextFragment("B1", id="b1")
    b2 = TextFragment("B2", id="b2")
    ha = HeaderFragment("A", id="ha")
    hb = HeaderFragment("B", id="hb")
    root = StructureNode(
        children=[
            StructureNode(value=ha, children=[StructureNode(value=a1), StructureNode(value=a2)]),
            StructureNode(value=hb, children=[StructureNode(value=b1), StructureNode(value=b2)]),
        ]
    )
    structure = DocumentStructure(root)
    return structure, {"ha": ha, "hb": hb, "a1": a1, "a2": a2, "b1": b1, "b2": b2}


def test_neighbors(sample_structure):
    """Fragments should navigate to their siblings correctly."""
    ds, fr = sample_structure
    assert ds.next(fr["ha"]) is fr["hb"]
    assert ds.previous(fr["hb"]) is fr["ha"]
    assert ds.next(fr["a1"]) is fr["a2"]
    assert ds.previous(fr["a2"]) is fr["a1"]
    assert ds.previous(fr["a1"]) is None
    assert ds.next(fr["a2"]) is None


def test_parent_children_and_leaf(sample_structure):
    """Validate parent/child relations and leaf detection."""
    ds, fr = sample_structure
    assert ds.parent(fr["a1"]) is fr["ha"]
    assert ds.parent(fr["ha"]) is None
    assert ds.children(fr["ha"]) == [fr["a1"], fr["a2"]]
    assert ds.children(fr["a1"]) == []
    assert ds.is_leaf(fr["a1"]) is True
    assert ds.is_leaf(fr["ha"]) is False


def test_invalid_fragment_errors(sample_structure):
    """Unknown fragments should raise ``ValueError`` for certain operations."""
    ds, _ = sample_structure
    with pytest.raises(ValueError):
        ds.children("missing")
    with pytest.raises(ValueError):
        ds.is_leaf("missing")


def test_levels(sample_structure):
    """Hierarchy level lookup works for fragments."""
    ds, fr = sample_structure
    assert ds.get_level(fr["ha"]) == 1
    assert ds.get_level(fr["a1"]) == 2


def test_lookup(sample_structure):
    """Lookup by id and content returns correct fragments."""
    ds, fr = sample_structure
    assert ds.get_fragment_by_id("b1") is fr["b1"]
    assert ds.get_fragment_by_content("B2") is fr["b2"]
    assert ds.get_fragment_by_id("missing") is None
    assert ds.get_fragment_by_content("zzz") is None


def test_structure_hierarchy_and_header(sample_structure):
    """Validate hierarchy flattening and header detection."""
    ds, fr = sample_structure
    assert ds.is_header(fr["ha"]) is True
    assert ds.is_header(fr["a1"]) is False

    assert ds.fragments == [fr["a1"], fr["a2"], fr["b1"], fr["b2"]]
    assert ds.structure == [
        (fr["ha"], 1),
        (fr["a1"], 2),
        (fr["a2"], 2),
        (fr["hb"], 1),
        (fr["b1"], 2),
        (fr["b2"], 2),
    ]

    df = ds.hierarchy()
    assert set(df.columns) == {"id", "parent_id", "level", "fragment"}
    assert len(df) == 6
    row = df[df["id"] == "a1"].iloc[0]
    assert row["parent_id"] == "ha"
    assert row["level"] == 2
    assert row["fragment"] is fr["a1"]


def test_from_level_pairs():
    """Construct structure from ``(level, fragment)`` pairs."""
    f1 = TextFragment("F1", id="f1")
    f2 = TextFragment("F2", id="f2")
    f3 = TextFragment("F3", id="f3")
    f4 = TextFragment("F4", id="f4")
    f5 = TextFragment("F5", id="f5")
    f6 = TextFragment("F6", id="f6")

    pairs = [
        (0, f1),
        (1, f2),
        (2, f3),
        (2, f4),
        (1, f5),
        (2, f6),
    ]

    ds = DocumentStructure.from_level_pairs(pairs)

    assert ds.structure == [
        (f1, 0),
        (f2, 1),
        (f3, 2),
        (f4, 2),
        (f5, 1),
        (f6, 2),
    ]
    assert ds.children(f1) == [f2, f5]
    assert ds.parent(f5) is f1
    assert ds.parent(f3) is f2
    assert ds.next(f3) is f4
    assert ds.previous(f5) is f2


def test_from_level_pairs_multiple_roots():
    """Multiple top-level nodes require a synthetic root."""
    a = TextFragment("A", id="a")
    b = TextFragment("B", id="b")
    ds = DocumentStructure.from_level_pairs([(0, a), (0, b)])

    assert ds.structure == [(a, 1), (b, 1)]
    assert ds.parent(a) is None
    assert ds.parent(b) is None
