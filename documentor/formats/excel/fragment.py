import datetime
from dataclasses import dataclass
from types import UnionType
from typing import Any
from overrides import overrides

from documentor.structuries.custom_types import LabelType
from documentor.structuries.fragment import Fragment


@dataclass
class SheetFragment(Fragment):
    """
    Class for fragments of sheet format document.
    Each fragment represents a cell of a sheet.

    :param value: contents of the cell
    :type value: int | float | str | datetime.datetime | datetime.date | None
    :param start_content: the original contents of the cell
    :type start_content: int | float | str | datetime.datetime | datetime.date | None
    :param relative_id: cell number (ignoring merged cells)
    :type relative_id: int
    :param type: cell content type
    :type type: int | str
    :param row: cell line number
    :type row: int
    :param column: cell column number
    :type column: int
    :param length: the length of the cell contents
    :type length: int
    :param vertically_merged: is the cell merged vertically
    :type vertically_merged: bool
    :param horizontally_merged: is the cell merged horizontally
    :type horizontally_merged: bool
    :param font_selection: is there a highlighted font in the cell
    :type font_selection: bool
    :param top_border: does the cell have a top border
    :type top_border: bool
    :param bottom_border: does the cell have a bottom border
    :type bottom_border: bool
    :param left_border: does the cell have a left border
    :type left_border: bool
    :param right_border: does the cell have a right border
    :type right_border: bool
    :param color: is the cell highlighted in color
    :type color: str | int
    :param font_color: is the font in the cell highlighted in color
    :type font_color: str | int
    :param is_formula: does the cell contain the formula
    :type is_formula: bool
    :param row_type: type of row on sheet
    :type row_type: int | None
    :param ground_truth: user-defined markup
    :type ground_truth: LabelType | None
    :param label: algorithmic markup
    :type label: LabelType | None
    """
    value: int | float | str | datetime.datetime | datetime.date | None
    start_content: int | float | str | datetime.datetime | datetime.date | None
    relative_id: int
    type: int | str
    row: int
    column: int
    length: int
    vertically_merged: bool
    horizontally_merged: bool
    font_selection: bool
    top_border: bool
    bottom_border: bool
    left_border: bool
    right_border: bool
    color: str | int
    font_color: str | int
    is_formula: bool
    row_type: int | None = None
    ground_truth: LabelType | None = None
    label: LabelType | None = None

    def __str__(self) -> int | float | str | datetime.datetime | datetime.date | None:
        """
        String representation of fragment's value.
        :return: value of fragment
        :rtype: str
        """
        return self.value

    @overrides
    def to_dict(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in self.__annotations__.keys()}

    @classmethod
    @overrides
    def param_types_dict(cls) -> dict[str, type | UnionType]:
        return {param: param_type for param, param_type in cls.__annotations__.items()}
