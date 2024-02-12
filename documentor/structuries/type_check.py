from collections.abc import Callable
from types import UnionType
from typing import Any, TypeVar
import pandas as pd

T = TypeVar('T')


class ErrorMessages:
    TYPE_ERROR = "Expected {expected}, got {actual} {optional_detail}"


def check_type_or_none_decorator(checker: Callable[[T], None]) -> Callable[[T], None]:
    def wrapper(obj: Any) -> None:
        if obj is not None:
            checker(obj)

    return wrapper


def raise_if_not_expected_type(obj: Any, expected_type: type | UnionType, optional_detail: str = ''):
    if not isinstance(obj, expected_type):
        raise TypeError(
            ErrorMessages.TYPE_ERROR.format(expected=expected_type, actual=type(obj), optional_detail=optional_detail))


def check_str(s: str) -> None:
    raise_if_not_expected_type(s, str)


def check_data_frame(df: pd.DataFrame) -> None:
    raise_if_not_expected_type(df, pd.DataFrame)


def check_dict_str_str(d: dict[str, str]) -> None:
    raise_if_not_expected_type(d, dict)
    for k, v in d.items():
        raise_if_not_expected_type(k, dict[str, str])
        raise_if_not_expected_type(v, str)


check_dict_str_str_or_none = check_type_or_none_decorator(check_dict_str_str)
