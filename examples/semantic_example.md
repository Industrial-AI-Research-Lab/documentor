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

```python is_executing=true
import pandas as pd

import sys

sys.path.append('.')
sys.path.append('../')

from documentor.types.text.document import SimpleDocument
from documentor.semantic.models.wiki2vec import WikiWord2VecModel
from documentor.semantic.preprocessing.tokenization import tokenize
from documentor.semantic.preprocessing.lemmatization import lemmatize
```

```python
w2v_modell = WikiWord2VecModel()
PATH_TO_MODEL = '../../data/ruwiki_20180420_300d.pkl'
w2v_modell.load_weights(path=PATH_TO_MODEL)
```

```python
DATAFRAME_PATH = '../../data/text.csv'
row_df = pd.read_csv(DATAFRAME_PATH).head(1000)
row_df
```

```python
document = SimpleDocument(row_df)
lemmatize(document)
tokenize(document, w2v_modell)

document
```

```python
specialized_terms = document.find_terms()
specialized_terms
```
