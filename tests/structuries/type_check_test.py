from typing import Any

import pandas as pd
import pytest

from documentor.structuries.type_check import TypeChecker


def test_check_simple_type_string():
    """
    Test that the check_simple_type function works for string objects
    """
    obj = "Test String"
    expected_type = str
    TypeChecker.check_simple_type(obj, expected_type)


def test_check_simple_type_int():
    """
    Test that the check_simple_type function works for integer objects
    """
    obj = 10
    expected_type = int
    TypeChecker.check_simple_type(obj, expected_type)


def test_check_simple_type_exception():
    """
    Test that the check_simple_type function raises an exception for incorrect types
    """
    obj = 'I am not an int'
    expected_type = int
    with pytest.raises(TypeError):
        TypeChecker.check_simple_type(obj, expected_type)


def test_check_str():
    """
    Test `check_str` function to ensure it correctly identifies input type as str
    """

    # Define a series of test examples and expected outputs
    test_inputs = ["this is a string", 14, True, None, 9.6, []]
    expected_outputs = [None, TypeError, TypeError, TypeError, TypeError, TypeError]

    # Hard loop over test examples and check against expected output
    for test, output in zip(test_inputs, expected_outputs):
        if isinstance(output, type) and issubclass(output, Exception):
            with pytest.raises(output):
                TypeChecker.check_str(test)
        else:
            assert TypeChecker.check_str(test) == output

    """
    Test check_data_frame_type method of TypeChecker with a valid DataFrame.
    """
    df = pd.DataFrame({'Name': ['John Doe', 'Jane Doe'], 'Age': [30, 25]})
    # Expect no exception
    TypeChecker.check_data_frame_type(df)


def test_check_data_frame_type_with_non_dataframe_string():
    """
    Test check_data_frame_type method of TypeChecker with a string.
    """
    not_df = "This is not a DataFrame"
    # Expect TypeError exception
    with pytest.raises(TypeError):
        TypeChecker.check_data_frame_type(not_df)


def test_check_data_frame_type_with_non_dataframe_list():
    """
    Test check_data_frame_type method of TypeChecker with a list.
    """
    not_df = ['This', 'is', 'not', 'a', 'DataFrame']
    # Expect TypeError exception
    with pytest.raises(TypeError):
        TypeChecker.check_data_frame_type(not_df)


def test_check_data_frame_type_with_non_dataframe_dictionary():
    """
    Test check_data_frame_type method of TypeChecker with a dictionary.
    """
    not_df = {'This': 1, 'is': 2, 'not': 3, 'a': 4, 'DataFrame': 5}
    # Expect TypeError exception
    with pytest.raises(TypeError):
        TypeChecker.check_data_frame_type(not_df)


def test_raise_if_not_expected_type():
    # Test with integer value matches expected type
    TypeChecker._raise_if_not_expected_type(5, int)

    # Test when object type doesn't match with expected type and should raise TypeError
    with pytest.raises(TypeError):
        TypeChecker._raise_if_not_expected_type(5, str)

    # Test with union types, as method also must work with Unions
    TypeChecker._raise_if_not_expected_type("Hello, World!", str | int)

    # Test with union types, where type doesn't match any in union and should raise TypeError
    with pytest.raises(TypeError):
        TypeChecker._raise_if_not_expected_type("Hello, World!", list | dict)

    # Test when object is None and expected type is NoneType
    TypeChecker._raise_if_not_expected_type(None, type(None))

    # Test when object is None but expected type is int, should raise TypeError
    with pytest.raises(TypeError):
        TypeChecker._raise_if_not_expected_type(None, int)


def test_check_type_or_none_decorator():
    def dummy_checker(obj: Any) -> None:
        if not isinstance(obj, int):
            raise TypeError('obj must be of type int')

    wrapped_checker = TypeChecker.check_type_or_none_decorator(dummy_checker)
    wrapped_checker(5)
    wrapped_checker(None)

    with pytest.raises(TypeError) as e_info:
        wrapped_checker('string')  # should raise error

    assert "obj must be of type int" in str(e_info.value)
