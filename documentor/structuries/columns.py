from dataclasses import dataclass
from types import UnionType


@dataclass
class ColumnType:
    """
    Class for checking type of column in DataFrame.

    If type is None or UnionType with None, then column is not required (required=False).

    :param type: expected type of column or several types in form of UnionType
    :type type: type | UnionType
    :param required: if column is required or not
    :type required: bool | None
    """
    type: type | UnionType
    required: bool | None = True

    def __post_init__(self):
        if isinstance(None, self.type):
            self.required = False
