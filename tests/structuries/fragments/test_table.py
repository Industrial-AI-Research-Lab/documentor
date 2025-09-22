import pytest
from PIL import Image

from documentor.data.structures.fragment.table import TableFragment, ImageTableFragment
from documentor.data.structures.fragment.description import TABLE


@pytest.mark.parametrize(
    "table,expected_str",
    [
        (
            [[1, 2, 3], ["a", "b", "c"]],
            "1 | 2 | 3\na | b | c",
        ),
        (
            [["один", 2], [3.14, True]],
            "один | 2\n3.14 | True",
        ),
    ],
)
def test_table_fragment_str_and_dict(table, expected_str):
    frag = TableFragment(value=table)
    assert str(frag) == expected_str

    d = frag.__dict__()
    assert d["value"] == table
    assert d["value_types"] is None
    assert d["cell_params"] is None
    assert d["column_separators"] == " | "
    assert d["row_separator"] == "\n"


@pytest.mark.parametrize(
    "table,value_types,cell_params,expected_types",
    [
        (
            [[1, "x"], [2.0, False]],
            [[int, str], [float, bool]],
            [[{"bold": True}, {}], [{}, {"color": "red"}]],
            [int, str, float, bool],
        ),
        (
            [["x"]],
            None,
            None,
            [str],
        ),
    ],
)
def test_table_fragment_get_all_params(table, value_types, cell_params, expected_types):
    frag = TableFragment(value=table, value_types=value_types, cell_params=cell_params)
    all_params = frag.get_all_params()

    assert [p["type"] for p in all_params] == expected_types
    # Ensure mapping of values preserved
    flat_values = [v for row in table for v in row]
    assert [p["value"] for p in all_params] == flat_values


@pytest.mark.parametrize("fname", ["single_table.png"])
def test_image_table_fragment_description_and_base64(fname, data_dir):
    img = Image.open(data_dir / "fragments" / fname)
    frag = ImageTableFragment(value=img)
    assert frag.description() == TABLE
    # Ensure base64 conversion works
    s = str(frag)
    assert isinstance(s, str) and len(s) > 10
