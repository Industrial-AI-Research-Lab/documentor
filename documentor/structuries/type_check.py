from collections.abc import Callable
from types import UnionType
from typing import Any, TypeVar

import pandas as pd

from documentor.structuries.columns import ColumnType

T = TypeVar('T')


class StaticClassMeta(type):
    """
    Metaclass for static classes. It prevents instantiation of classes.
    """

    def __call__(cls, *args, **kwargs):
        raise TypeError("Cannot instantiate a static class")


class ErrorMessages(StaticClassMeta):
    """
    Static class with error messages for type checking.
    """
    TYPE_ERROR = "Expected {expected}, got {actual}"
    COLUMN_NOT_IN_DF = "Column {column_name} is not in DataFrame"
    COLUMN_TYPE_ERROR = "Column {column_name} has wrong type. Expected {expected}, got {actual}"


class TypeChecker(metaclass=StaticClassMeta):
    """
    Static class for type checking.
    """
    @staticmethod
    def check_str(s: Any) -> None:
        """
        Check if object is of type str.

        :param s: object to check
        :type s: Any
        :return:
        :rtype: None
        :raises TypeError: if object is not of type str
        """
        _raise_if_not_expected_type(s, str)

    @staticmethod
    def check_data_frame_type(df: Any) -> None:
        """
        Check if object is of type pd.DataFrame.

        :param df:
        :return:
        :rtype: None
        :raises TypeError: if object is not of type pd.DataFrame
        """
        _raise_if_not_expected_type(df, pd.DataFrame)

    @staticmethod
    def check_df_column(df: pd.DataFrame, column_name: str, column_type: ColumnType) -> None:
        """
        Check if column in DataFrame has the right type.

        :param df: DataFrame
        :type df: pd.DataFrame
        :param column_name: name of column
        :type column_name: str
        :param column_type: type of column
        :type column_type: ColumnType
        :return: None
        :raises TypeError: if column has wrong type
        :raises ValueError: if column is not in DataFrame
        """
        if column_name not in df.columns:
            if column_type.required:
                raise ValueError(f"Column {column_name} is not in DataFrame")
            else:
                return
        if not isinstance(df[column_name].dtype, column_type.type):
            raise TypeError(
                f"Column {column_name} has wrong type. Expected {column_type.type}, got {df[column_name].dtype}")

    @staticmethod
    def check_data_frame_columns(df: pd.DataFrame, columns: dict[str, ColumnType]) -> None:
        """
        Check if DataFrame has all required columns and if they have right types.

        :param df: DataFrame
        :type df: pd.DataFrame
        :param columns: dictionary with column names and their types
        :type columns: dict[str, ColumnType]
        :return:
        :rtype: None
        :raises ValueError: if DataFrame does not have required columns
        :raises TypeError: if columns have wrong types
        """
        for column_name, column_type in columns.items():
            TypeChecker.check_df_column(df, column_name, column_type)


def _raise_if_not_expected_type(obj: Any, expected_type: type | UnionType) -> None:
    """
    Raise TypeError if object is not of expected type.

    :param obj: object to check
    :type obj: Any
    :param expected_type: type to check or sewer of types in form of UnionType
    :type expected_type: type | UnionType
    :return:
    :rtype: None
    :raises TypeError: if object is not of expected type
    """
    if not isinstance(obj, expected_type):
        raise TypeError(
            ErrorMessages.TYPE_ERROR.format(expected=expected_type, actual=type(obj)))


def check_type_or_none_decorator(checker: Callable[[T], None]) -> Callable[[T], None]:
    """
    Decorator for checking if object is of expected type or None.

    :param checker: function for checking type
    :type checker: Callable[[T], None]
    :return: wrapped function which check object type if it is not None
    :rtype: Callable[[T], None]
    """

    def wrapper(obj: Any) -> None:
        if obj is not None:
            checker(obj)

    return wrapper
