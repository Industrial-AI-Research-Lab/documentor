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

# Example of using the algorithm to search for specialized terms

```python is_executing=true
import sys

sys.path.append('../notebooks')
sys.path.append('../')
```

Imports methods, classes and entities from documentor

```python
import pandas as pd

from documentor.formats.text.document import SimpleDocument
from documentor.semantic.models.wiki2vec import WikiWord2VecModel
from documentor.semantic.preprocessing.tokenization import tokenize
from documentor.semantic.preprocessing.lemmatization import lemmatize
```

Loading models weights and data for processing 

```python is_executing=true
# size of weights - 5GB. 
# It can take quite a while to download


# !cd ../../data
# !wget https://drive.google.com/file/d/1ROoM7__3100Ts3uU2uMVZUFdobKt13zd/view?usp=sharing
```

```python
w2v_model = WikiWord2VecModel()
PATH_TO_MODEL = '../../data/ruwiki_20180420_300d.pkl'
w2v_model.load_weights(path=PATH_TO_MODEL)
```

```python is_executing=true
DATAFRAME_PATH = '../examples/data/work_names.csv'
row_df = pd.read_csv(DATAFRAME_PATH).head(1000)
row_df
```

Text preprocessing

```python is_executing=true
# create a SimpleDocument entity
document = SimpleDocument(row_df)

# Lemmatize text of document using natasha
lemmatize(document)

# Get embeddings for lemmatized text
tokenize(document, w2v_model)

document
```

Find a specialized terms in processed texts

```python
specialized_terms = document.find_terms()
specialized_terms
```
