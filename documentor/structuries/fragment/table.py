"""
Table fragment implementations.

Contains:
- ImageTableFragment: table recognized within an image region.
- TableFragment: structured 2D data with optional cell typing/params.
"""
from dataclasses import dataclass
from typing import Any

from .base import Fragment
from .description import TABLE
from .image import ImageFragment


@dataclass
class ImageTableFragment(ImageFragment):
    """
    Implementation for table fragments that have an image value.
    Each instance of this class represents a table in the image.

    Attributes:
        value (PIL.Image.Image): The image content of the table region.
        format (str): Image format used for serialization.
        encoding (str): Text encoding used for base64 conversion.
        description (str): Fragment type description for LLMs.
    """
    description: str = TABLE
    is_processed: bool = False

@dataclass
class TableFragment(Fragment):
    """
    Implementation for table fragments that have a 2D list value.
    Each instance of this class represents a table in the document.

    Attributes:
        value (list[list[Any]]): 2D array of cell values.
        value_types (list[list[type]] | None): Optional 2D array of cell value types.
        cell_params (list[list[dict[str, Any]]] | None): Optional 2D array of cell parameters.
        column_separators (str): Separator used when converting the table to string.
        row_separator (str): Row separator used when converting the table to string.
        description (str): Fragment type description for LLMs.
        need_to_recognize (bool): Indicates if recognition is required for this fragment.
    """
    value: list[list[Any]]
    value_types: list[list[type]] | None = None
    cell_params: list[list[dict[str, Any]]] | None = None

    column_separators: str = ' | '
    row_separator: str = '\n'

    description: str = TABLE

    def __str__(self) -> str:
        """
        String representation of the table fragment value.

        Returns:
            str: String representation of the table.
        """
        return self.row_separator.join(
            [self.column_separators.join(map(str, row)) for row in self.value]
        )

    def __dict__(self) -> dict[str, Any]:
        """Get parameters of the table fragment."""
        data = super().__dict__()
        data.update({
            "value_types": self.value_types,
            "cell_params": self.cell_params,
            "column_separators": self.column_separators,
            "row_separator": self.row_separator,
        })
        return data

    def get_all_params(self) -> list[dict[str, Any]]:
        """
        Get values, types, and parameters of all cells in the table.
        Returns:
            list[dict[str, Any]]: List of dictionaries with cell value, type, and parameters:
                "value": cell value
                "type": cell type
                "params": cell parameters
        """
        all_params = []
        for i, row in enumerate(self.value):
            for j, cell in enumerate(row):
                cell_param = {
                    "value": cell,
                    "type": self.value_types[i][j] if self.value_types else type(cell),
                    "params": self.cell_params[i][j] if self.cell_params else {}
                }
                all_params.append(cell_param)
        return all_params
