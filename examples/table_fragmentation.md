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

Import the necessary classes and libraries.

```python
from documentor.types.excel.classifier import SheetFragmentClassifier

import pandas as pd
import warnings
warnings.filterwarnings('ignore')
```

Importing a class for the classifier of sheet format fragments.

```python
classifier = SheetFragmentClassifier()
```

Getting a parsed and marked-up file.

```python
hot_list_df = pd.read_csv('data/processed_tables/hot_list_parsed.csv', index_col='Unnamed: 0')
```

Clustering and data markup.

```python
classifier.devide_and_cluster(hot_list_df)
```
