from datetime import datetime, date

import pytest

from documentor.structuries.custom_types import LabelType
from documentor.types.excel.fragment import SheetFragment
from tests.document.excel.parameters import FRAGMENT_VALUES_PARAMETRIZER, FRAGMENT_POST_INIT_PARAMETRIZER, FRAGMENT_STR_PARAMETRIZER


@pytest.mark.parametrize('test_values', FRAGMENT_VALUES_PARAMETRIZER)
def test_to_dict(test_values):
    fragment = SheetFragment(**test_values)

    result = fragment.to_dict()
    assert isinstance(result, dict)
    assert result == test_values


@pytest.mark.parametrize(
    "kwargs, expected_attrs",
    FRAGMENT_POST_INIT_PARAMETRIZER,
)
def test_fragment_post_init(kwargs, expected_attrs):
    fragment = SheetFragment(**kwargs)

    for attr, expected_value in expected_attrs.items():
        assert getattr(fragment, attr) == expected_value


@pytest.mark.parametrize('fragment_item, expected_output', FRAGMENT_STR_PARAMETRIZER)
def test_fragment_str(fragment_item, expected_output):
    assert str(fragment_item) == expected_output


def test_param_types_dict():
    # Getting the param types dictionary
    param_types = SheetFragment.param_types_dict()

    # Assertion Basics
    assert isinstance(param_types, dict)
    assert len(param_types) == 20

    # Checking each item in the dict
    assert param_types.get('value') == int | float | str | datetime | date | None
    assert param_types.get('start_content') == int | float | str | datetime | date | None
    assert param_types.get('relative_id') == int
    assert param_types.get('type') == int | str
    assert param_types.get('row') == int
    assert param_types.get('column') == int
    assert param_types.get('length') == int
    assert param_types.get('vertically_merged') == bool
    assert param_types.get('horizontally_merged') == bool
    assert param_types.get('font_selection') == bool
    assert param_types.get('top_border') == bool
    assert param_types.get('bottom_border') == bool
    assert param_types.get('left_border') == bool
    assert param_types.get('right_border') == bool
    assert param_types.get('color') == str | int
    assert param_types.get('font_color') == str | int
    assert param_types.get('is_formula') == bool
    assert param_types.get('row_type') == int | None
    assert param_types.get('ground_truth') == LabelType | None
    assert param_types.get('label') == LabelType | None