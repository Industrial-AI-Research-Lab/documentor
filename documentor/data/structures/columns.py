from dataclasses import dataclass
from types import UnionType


@dataclass
class ColumnType:
    """
    Class for checking the type of a column in a DataFrame.

    If type is None or a UnionType including None, then the column is not required (required=False).

    Args:
        type (type | UnionType): Expected type of the column or a Union of types.
        required (bool | None, optional): Whether the column is required. Defaults to True.
    """
    type: type | UnionType
    required: bool | None = True

    # def __post_init__(self):
    #    if isinstance(None, self.type):
    #        self.required = False
