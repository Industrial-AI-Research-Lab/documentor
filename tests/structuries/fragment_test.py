import pytest

from documentor.structuries.custom_types import LabelType, VectorType
from documentor.structuries.fragment import TextFragment
from tests.structuries.parameters import FRAGMENT_POST_INIT_PARAMETRIZER, FRAGMENT_STR_PARAMETRIZER, \
    FRAGMENT_VALUES_PARAMETRIZER


@pytest.mark.parametrize(
    "kwargs, expected_attrs",
    FRAGMENT_POST_INIT_PARAMETRIZER,
)
def test_fragment_post_init(kwargs, expected_attrs):
    fragment = TextFragment(**kwargs)

    for attr, expected_value in expected_attrs.items():
        assert getattr(fragment, attr) == expected_value


@pytest.mark.parametrize('fragment_item, expected_output', FRAGMENT_STR_PARAMETRIZER)
def test_fragment_str(fragment_item, expected_output):
    assert str(fragment_item) == expected_output


def create_fragment_and_compare_with_dict(test_values: dict):
    fragment = TextFragment(**test_values)

    result = fragment.__dict__()
    assert isinstance(result, dict)
    assert result == test_values


@pytest.mark.parametrize('test_values', FRAGMENT_VALUES_PARAMETRIZER)
def test_to_dict(test_values):
    fragment = TextFragment(**test_values)

    result = fragment.__dict__()
    assert isinstance(result, dict)
    assert result == test_values

