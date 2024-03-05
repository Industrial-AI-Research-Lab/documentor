import pytest

from documentor.structuries.custom_types import LabelType, VectorType
from documentor.structuries.fragment import Fragment
from tests.structuries.parameters import FRAGMENT_POST_INIT_PARAMETRIZER, FRAGMENT_STR_PARAMETRIZER, \
    FRAGMENT_VALUES_PARAMETRIZER


@pytest.mark.parametrize(
    "kwargs, expected_attrs",
    FRAGMENT_POST_INIT_PARAMETRIZER,
)
def test_fragment_post_init(kwargs, expected_attrs):
    fragment = Fragment(**kwargs)

    for attr, expected_value in expected_attrs.items():
        assert getattr(fragment, attr) == expected_value


@pytest.mark.parametrize('fragment_item, expected_output', FRAGMENT_STR_PARAMETRIZER)
def test_fragment_str(fragment_item, expected_output):
    assert str(fragment_item) == expected_output


def create_fragment_and_compare_with_dict(test_values: dict):
    fragment = Fragment(**test_values)

    result = fragment.to_dict()
    assert isinstance(result, dict)
    assert result == test_values


@pytest.mark.parametrize('test_values', FRAGMENT_VALUES_PARAMETRIZER)
def test_to_dict(test_values):
    fragment = Fragment(**test_values)

    result = fragment.to_dict()
    assert isinstance(result, dict)
    assert result == test_values


def test_param_types_dict():
    # Getting the param types dictionary
    param_types = Fragment.param_types_dict()

    # Assertion Basics
    assert isinstance(param_types, dict)
    assert len(param_types) == 6

    # Checking each item in the dict
    assert param_types.get('value') == str
    assert param_types.get('ground_truth') == LabelType | None
    assert param_types.get('label') == LabelType | None
    assert param_types.get('vector') == VectorType | None
    assert param_types.get('tokens') == list[str] | None
    assert param_types.get('token_vectors') == list[VectorType] | None
