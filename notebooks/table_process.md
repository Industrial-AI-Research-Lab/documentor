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
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
from copy import copy
from sklearn.preprocessing import normalize
import numpy as np

from documentor.sheets.parser import SheetParser
```

Парсинг исходного файла

```python is_executing=true
a = SheetParser()
d = a.parse_file(path='start_tables/D2.xlsx', sheet_name='Ресурсы', first_cell='A1', last_cell='CT62')
d.doc_df
```

```python
a.to_csv(d, 'processed_tables/new_resources.xlsx')
```

```python
def context_processing(context):
    hased_context = [[hash(tuple(x)) for x in cont] for cont in context]
    normalized_context = []
    for x in hased_context:
        if len(x) > 0:
            normalized_context.append(normalize([x]))
        else:
            normalized_context.append(0)
    average_context = [np.average(x) for x in normalized_context]
    return average_context
```

```python
def row_col_context(context: list, index: int):
    for r in copy(context):
        diff = r[3] - index
        r.append(diff)
        if diff > 0:
            r.append(0)
        elif diff < 0:
            r.append(1)
        else:
            context.remove(r)
    return context
```

```python
last_row = d.doc_df.Row.tail(1).values[0]
last_col = d.doc_df.Column.tail(1).values[0]
row_context = []
col_context = []
env_cont = []
```

```python
names = list(d.doc_df.columns)
c_i = names.index('Column')
r_i = names.index('Row')
for source_i, source_row in enumerate(d.doc_df.itertuples()):
    row_index = source_row[r_i+1]
    index_row = [*range(int(row_index) - 10, int(row_index) + 10)]
    col_index = source_row[c_i+1]
    index_col = [*range(int(col_index) - 10, int(col_index) + 10)]
    for id in copy(index_row):
        if id < 0 or id > last_row:
            index_row.remove(id)
    for id in copy(index_col):
        if id < 0 or id > last_col:
            index_col.remove(id)
    row_env = [*range(int(col_index) - 3, int(col_index) + 3)]
    col_env = [*range(int(row_index) - 3, int(row_index) + 3)]

    rows = d.doc_df.loc[(d.doc_df['Row'] == row_index) & (d.doc_df['Column'].isin(index_col))]
    cols = d.doc_df.loc[(d.doc_df['Column'] == col_index) & (d.doc_df['Row'].isin(index_row))]

    environment = d.doc_df.loc[(d.doc_df['Column'].isin(row_env)) & \
                             (d.doc_df['Row'].isin(col_env))]  # square

    r_context = rows.values.tolist()
    c_context = cols.values.tolist()
    env_context = environment.values.tolist()

    for env in copy(env_context):
        diff = (env[2] + env[3]) - (row_index + col_index)
        env.append(diff)
        if env[3] < col_index and env[2] < row_index:
            env.append(0)
        elif env[3] > col_index and env[2] < row_index:
            env.append(1)
        elif env[3] > col_index and env[2] > row_index:
            env.append(2)
        elif env[3] < col_index and env[2] > row_index:
            env.append(3)
        elif env[3] == col_index and env[2] > row_index:
            env.append(4)
        elif env[3] == col_index and env[2] < row_index:
            env.append(5)
        elif env[3] < col_index and env[2] == row_index:
            env.append(6)
        elif env[3] > col_index and env[2] == row_index:
            env.append(7)
        else:
            env_context.remove(env)

    row_context.append(row_col_context(r_context, col_index))
    col_context.append(row_col_context(c_context, row_index))
    env_cont.append(env_context)
```

```python
d.doc_df['row_context'] = context_processing(row_context)
d.doc_df['col_context'] = context_processing(col_context)
d.doc_df['env_context'] = context_processing(env_cont)
```
