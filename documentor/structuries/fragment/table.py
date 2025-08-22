from dataclasses import dataclass
from typing import Any

from documentor.structuries.fragment import FragmentInterface
from documentor.structuries.fragment.description import TABLE


@dataclass
class TableFragment(FragmentInterface):
    """
    Implementation for table fragments that have a 2D list value.
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
        """
        Get parameters of the table fragment.
        """
        return {
            "value": self.value,
            "value_types": self.value_types,
            "cell_params": self.cell_params,
            "column_separators": self.column_separators,
            "row_separator": self.row_separator
        }

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

