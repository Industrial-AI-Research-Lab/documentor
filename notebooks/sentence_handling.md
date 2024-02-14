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
!pip install idbadapter
```

```python
!pip install -U sentence-transformers
```

## Tokenizer

```python
import numpy as np
```

```python
!pip install numpy
```

```python

```

```python
from sentence_transformers import SentenceTransformer
sentences = ["This is an example sentence", "Each sentence is converted"]

model = SentenceTransformer('uaritm/multilingual_en_ru_uk')
embeddings = model.encode(sentences)
def get_embs(sentence):
    model.encode(sentence)

```

```python

```

```python
from idbadapter import Schedules
import pandas as pd
import wikipedia
```

```python
URL = "postgresql+psycopg2://testuser:pwd@10.32.15.30:25432/test"
adapter = Schedules(URL)
```

```python
work_names = adapter.get_all_works_name()
res_names = adapter.get_resources_names()
```

```python
res_names
```

```python
work_names[['name', 'processed_name']]
```

```python
work_names_embs = model.encode(work_names['granulary_name'])
# res_names_embs = model.encode(res_names['granulary_name'])
```

```python
# work_names_embs.shap
work_names_embs.shape                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
```

### Visualization

```python
from sklearn.manifold import TSNE
import numpy as np

tsne = TSNE(n_components=2, random_state=0)

def decrease_dimension(data, n_components=2):
    tsne = TSNE(n_components=n_components, random_state=0)
    return tsne.fit_transform(data)

```

```python
w_embeddings_2d = decrease_dimension(work_names_embs, n_components=2)
```

```python
norms = np.linalg.norm(w_embeddings_2d, axis=1)

normalized_vectors = w_embeddings_2d / norms[:, np.newaxis]

normalized_vectors
```

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 8))
plt.scatter(normalized_vectors[:, 0], normalized_vectors[:, 1], marker='.', alpha=1)
plt.title('2D Visualization of Text Embeddings using t-SNE')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.show()
```

clustering row embs


```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize





```

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize


def calculate_wcss(data):
    wcss = []
    for n in range(1, 11):
        kmeans = KMeans(n_clusters=n, random_state=0)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)
    return wcss

def optimal_number_of_clusters(wcss):
    x1, y1 = 2, wcss[0]
    x2, y2 = 20, wcss[len(wcss)-1]

    distances = []
    for i in range(len(wcss)):
        x0 = i+2
        y0 = wcss[i]
        numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
        denominator = np.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        distances.append(numerator/denominator)
    
    return distances.index(max(distances)) + 2


```

```python
# Пример использования:
# embeddings = np.array([...]) # ваш массив эмбеддингов слов
def find_n_clusters(embs):
    normalized_embeddings = normalize(embs)
    wcss = calculate_wcss(normalized_embeddings)
    n = optimal_number_of_clusters(wcss)

    return n
```

```python
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

def kmeans_clustering_embeddings(embeddings, num_clusters):

    normalized_embeddings = normalize(embeddings)

    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(normalized_embeddings)

    return kmeans.labels_
```

```python
clustering = kmeans_clustering_embeddings(work_names_embs, num_clusters=11)
```

```python
clustering
```

```python
work_names[['x', 'y']] = w_embeddings_2d
```

```python
work_names['cluster'] = clustering
```

```python
work_names
```

```python

norms = np.linalg.norm(w_embeddings_2d, axis=1)

normalized_vectors = w_embeddings_2d / norms[:, np.newaxis]

normalized_vectors



```

```python
fig = px.scatter(data_frame=work_names, x='x', y='y', hover_name='granulary_name', color='cluster')

fig.show()
```

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
plt.scatter(w_embeddings_2d[:, 0], w_embeddings_2d[:, 1], marker='.', alpha=0.5)
plt.title('2D Visualization of Text Embeddings using t-SNE')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.show()
```

# Excel Experiment

```python
work_names = adapter.get_all_works_name()
xl_data_df = pd.read_excel('xl_test.xlsx', sheet_name='НН', index_col=None, header=None)
xl_data_df.shape
xl_data = xl_data_df.to_numpy()
df = pd.DataFrame()
```

```python
xl_data = xl_data.flatten()
xl_data.shape
```

```python
xl_data = [k for k in xl_data.tolist() if type(k) is str]

```

```python
arr = np.array(xl_data).astype(str)
arr
```

```python
arr.shape
```

```python
xl_df
```

```python

```

```python
def main(df):
    # embeddings
    df_embs = df_embs = model.encode(df['name'])
    
    # normalize
    norms = np.linalg.norm(df_embs, axis=1)
    normalized_vectors = df_embs / norms[:, np.newaxis]
    embs_2d = decrease_dimension(data=normalized_vectors)
    
    # clustering
    n_classes = find_n_clusters(df_embs)
    print(n_classes)
    clustering = kmeans_clustering_embeddings(df_embs, num_clusters=n_classes)
    df['cluster'] = clustering
    # tsne
    embs_2d = decrease_dimension(data=df_embs)
    df[['x', 'y']] = embs_2d
    
    return df

```

```python
xl_df = pd.DataFrame()
work_names['marker'] = 0
xl_df['name'] = arr
xl_df['marker'] = 1
df = pd.concat([work_names[['name', 'marker']], xl_df[['name', 'marker']]], ignore_index=True, )
df.dropna(inplace=True)
df
```

```python
new_df = main(df)
```

```python
fig = px.scatter(data_frame=new_df, x='x', y='y', hover_name='name', color='cluster', width=1800, height=1600)
fig.update_traces(marker_size=6)

fig.show()
```

# Download Wiki

```python

```

```python
def get_articles(df):
    wikipedia.set_lang('ru')
    names = df['processed_name'].values.tolist()
    for name in names:
        try:
            articles = [wikipedia.search(n) for n in name.split()]
            data = [wikipedia.page(ar).content for ar in articles]
        except Exception:
            continue
        yield "__end of page__".join(data)
        
```

```python
wikipedia.set_lang('ru')

```

```python

for k in get_articles(work_names):
    with open('texts.txt', 'a', encoding='UTF-8') as f:
        print(k, file=f)

```

```python
with open('texts.txt', 'r', encoding='UTF-8') as f:
    texts = f.read().split("__end of page__")

texts    
```

```python
embeddings = model.encode(texts)
```

```python
embeddings
```

```python
def cosine_similarity(vecA, vecB):
    dot_product = np.dot(vecA, vecB)
    norm_a = np.linalg.norm(vecA)
    norm_b = np.linalg.norm(vecB)
    return dot_product / (norm_a * norm_b)

```

```python
def search_terms(query, text_embs):
    query_embs = model.encode(query)
    similarities = [cosine_similarity(query_embs, text_embedding) for text_embedding in text_embs]
    return similarities
    
```

```python
test = search_terms('Аквапарк', embeddings)
np.max(test)
```

```python

```
