---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.1
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell import Cell
from typing import Iterable, List, Dict, Any
from openpyxl.styles import PatternFill
```

## Load Data

```python
test = openpyxl.load_workbook('../examples/data/test.xlsx', data_only=True)
sheet_test = test['Лист1']

global_hot = openpyxl.load_workbook('../examples/data/Global_Hot_List.xlsx', data_only=True)
hotlist_compl = global_hot['Hotlist - Identified ']
```

## Meta information parser

```python
def meta_parser(sheet: Worksheet) -> dict:
    """
    Parse metadata of each cell in the given worksheet.
    
    :param sheet: The worksheet to parse.
    :type sheet: Worksheet
    :return: A dictionary containing metadata for each cell in the worksheet.
             The keys are cell addresses (e.g., 'A1', 'B2') and the values are dictionaries
             with the following keys:
               - 'value': The value of the cell.
               - 'data_type': The data type of the cell value.
               - 'borders': A dictionary containing border styles for top, right, bottom, and left borders.
                            Each border style can be one of 'thin', 'medium', 'thick', 'double', 'dashed',
                            'dotted', 'dashDot', 'dashDotDot', 'mediumDashed', 'slantDashDot', 'hair',
                            'mediumDashDotDot', 'mediumDashDot', 'mediumDash', or None if no border.
               - 'neighbors': A dictionary containing values of neighboring cells in the worksheet.
                              The keys represent the relative position of the neighboring cell, and the values
                              are the values of those cells. Possible keys are 'above', 'below', 'left',
                              'right', 'upper_left', 'upper_right', 'lower_left', 'lower_right'.
                              If a neighboring cell is empty or out of bounds, its value will be None.
    """
    cell_info = {}
    for row in sheet.iter_rows():
        for cell in row:
            cell_address = cell.coordinate
    
            cell_value = cell.value
    
            cell_data_type = type(cell_value).__name__
    
            borders = {
                "top": cell.border.top.style if cell.border.top.style else None,
                "right": cell.border.right.style if cell.border.right.style else None,
                "bottom": cell.border.bottom.style if cell.border.bottom.style else None,
                "left": cell.border.left.style if cell.border.left.style else None
            }
    
    
            column_index = cell.column
            row_index = cell.row
    
            def get_value(sheet: Worksheet, column_index: int, row_index: int) -> any:
                """
                Get the value of the cell at the specified column and row indices in the given worksheet.
                
                :param sheet: The worksheet to retrieve the cell value from.
                :type sheet: Worksheet
                :param column_index: The column index of the cell.
                :type column_index: int
                :param row_index: The row index of the cell.
                :type row_index: int
                :return: The value of the cell at the specified indices, or None if the indices are out of bounds.
                :rtype: any
                """
                if column_index < 1 or row_index < 1:
                    return None
                return sheet[get_column_letter(column_index) + str(row_index)].value
    
            neighbor_cells = {
                "above": get_value(sheet, column_index, row_index - 1),
                "below": get_value(sheet, column_index, row_index + 1),
                "left": get_value(sheet, column_index - 1, row_index),
                "right": get_value(sheet, column_index + 1, row_index),
                "upper_left": get_value(sheet, column_index - 1, row_index - 1),
                "upper_right": get_value(sheet, column_index + 1, row_index - 1),
                "lower_left": get_value(sheet, column_index - 1, row_index + 1),
                "lower_right": get_value(sheet, column_index + 1, row_index + 1)
            }
    
            cell_info[cell_address] = {
                "value": cell_value,
                "data_type": cell_data_type,
                "borders": borders,
                "neighbors": neighbor_cells
            }
    return cell_info
```

```python
for cell_address, info in meta_parser(sheet_test).items():
        print(f"Ячейка {cell_address}:")
        print(f"Значение: {info['value']}")
        print(f"Тип данных: {info['data_type']}")
        print(f"Границы: {info['borders']}")
        print(f"Соседние ячейки: {info['neighbors']}")
        print()
```

## Detect tables

```python
def detection_by_empty_row(sheet: Worksheet) -> List[Dict[str, Any]]:
    """
    Detect tables in the worksheet based on empty rows and columns.

    :param sheet: The worksheet to detect tables in.
    :type sheet: Worksheet
    :return: A list of dictionaries containing information about each detected table. Each dictionary has the following keys:
               - 'start_cell': The coordinate of the top-left cell of the table.
               - 'last_cell': The coordinate of the bottom-right cell of the table.
               - 'table': A 2D list representing the cells of the table.
    :rtype: List[Dict[str, Any]]
    """
    
    def is_row_empty(row: Iterable[Cell]) -> bool:
        """
        Check if a row is empty.

        :param row: An iterable containing cells of a row.
        :type row: Iterable[Cell]
        :return: True if the row is empty, False otherwise.
        :rtype: bool
        """
        for cell in row:
            value = cell.value
            left = cell.border.left.style if cell.border.left.style else None
            right = cell.border.right.style if cell.border.right.style else None

            if any(item is not None for item in [value, left, right]):
                return False
        return True
       

    def is_column_empty(table: List[List[Cell]], column_index: int) -> bool:
        """
        Check if a column in a table is empty.
        
        :param table: A 2D list representing cells of a table.
        :type table: List[List[Cell]]
        :param column_index: The index of the column to check.
        :type column_index: int
        :return: True if the column is empty, False otherwise.
        :rtype: bool
        """
        for row in table:
            value = row[column_index].value
            left = row[column_index].border.top.style if row[column_index].border.top.style else None
            right = row[column_index].border.bottom.style if row[column_index].border.bottom.style else None
            
            if any(item is not None for item in [value, left, right]):
                    return False
        return True
    
    def split_table_by_empty_columns(table: List[List[Cell]]) -> List[List[List[Cell]]]:
        """
        Split a table into subtables based on empty columns.

        :param table: A 2D list representing cells of a table.
        :type table: List[List[Cell]]
        :return: A list of subtables, where each subtable is represented as a 2D list of cells.
        :rtype: List[List[List[Cell]]]
        """
        subtables = []
        current_subtable = []
        columns_count = len(table[0])
        
        for end_col in range(columns_count):
            if is_column_empty(table, end_col):
                if current_subtable:  
                    subtables.append(current_subtable)
                    current_subtable = []
            else:
                for row_index, row in enumerate(table):
                    if len(current_subtable) <= row_index:
                        current_subtable.append([])
                    current_subtable[row_index].append(row[end_col])
        
        if current_subtable:
            subtables.append(current_subtable)
        
        return subtables
    
    tables = []
    current_table = []
    for row in sheet.iter_rows():
        if is_row_empty(row):
            if current_table:
                tables.extend(split_table_by_empty_columns(current_table))
                current_table = []
        else:
            current_table.append(row)
    if current_table:
        tables.extend(split_table_by_empty_columns(current_table))
    
    tables_info = []
    for i, table in enumerate(tables):
        start_cell = table[0][0].coordinate
        last_cell = table[-1][-1].coordinate
        tables_info.append(dict(start_cell=start_cell, last_cell=last_cell, table=table))
    
    return tables_info
```

```python
detection_by_empty_row(sheet_test)
```

```python
detection_by_empty_row(hotlist_compl)
```
