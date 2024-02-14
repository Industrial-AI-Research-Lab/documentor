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
from documentor.sheets.parser import SheetParser
from documentor.sheets.classifier import SheetFragmentClassifier

import pandas as pd
import warnings
warnings.filterwarnings('ignore')
```

```python
a = SheetParser()
d = a.from_file(path='start_tables/Global Hot List.xlsx', sheet_name='Hotlist - Identified ', first_cell='A5', last_cell='U75')
d.doc_df
```

```python
a.to_csv(d, 'processed_tables/HotList.csv', sep=",")
```

```python
parsed = pd.read_csv('processed_tables/HotList.csv', index_col='Unnamed: 0')
clustered = pd.read_csv('processed_tables/hot_list_parsed.csv')
parsed['cluster_name'] = clustered['cluster_name']
parsed.to_csv('processed_tables/hot_list_parsed.csv')
```

```python
parsed = pd.read_csv('processed_tables/hot_list_parsed.csv', index_col='Unnamed: 0')

classifier = SheetFragmentClassifier()
classifier.devide_and_cluster(parsed)
```

```python

```
