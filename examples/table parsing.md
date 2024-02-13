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
from documentor.types.excel.parser import SheetParser
```

```python
parser = SheetParser()
doc = parser.from_file(path='data/start_tables/Global Hot List.xlsx', sheet_name='Hotlist - Identified ', first_cell='A5', last_cell='U75')
doc.to_df()
```

```python
parser.to_csv(doc, 'data/processed_tables/Global Hot List.csv', sep=",")
```
