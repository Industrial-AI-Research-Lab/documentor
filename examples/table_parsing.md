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

Import of the class responsible for processing primary sheet documents.

```python
from documentor.types.excel.parser import SheetParser
```

Initialization of the parser.

```python
parser = SheetParser()
```

Parser processing of the file.

```python
doc = parser.parse_file(path='data/start_tables/Global Hot List.xlsx', sheet_name='Hotlist - Identified ', first_cell='A5', last_cell='U75')
```

Output of the resulting dataset.

```python
doc.to_df()
```

Saving the resulting dataset to a csv file.

```python
parser.to_csv(doc, 'data/processed_tables/Global Hot List.csv', sep=",")
```
