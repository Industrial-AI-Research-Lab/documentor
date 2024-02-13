from typing import Any

from documentor.structuries.fragment import Fragment
from documentor.structuries.type_check import check_str


class TextFragment(Fragment):
    """
    Simple realization of fragment with string value.

    Each fragment represents a structural unit of a document,
    for example, a table cell, a log entry, a paragraph of a document with a string value and parameters.

    :param value: value of fragment
    """
    _value: str

    @property
    def value(self) -> str:
        return self._value

    def __init__(self, value: str) -> None:
        """
        Simple realization of fragment with string value.

        :param value: value of fragment
        :type value: str
        :return: None
        :raises TypeError: if the object is not str
        """
        check_str(value)
        self._value = value

    def params(self) -> dict[str, Any]:
        """
        Returns an empty dictionary.
        :return: empty dictionary
        :rtype: dict
        """
        return {"value": self.value}
