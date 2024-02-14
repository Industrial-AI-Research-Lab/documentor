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
import numpy as np
import pandas as pd
from datetime import datetime, time
```

```python
new_df = pd.read_csv('processed_tables/2_parsed.csv', index_col='Unnamed: 0')
new_df
```

```python
ndf = pd.DataFrame()
ndf['Row'] = new_df['Row']
ndf['Column'] = new_df['Column']
ndf['Color'] = new_df['Color']
ndf['Vertically_merged'] = new_df['Vertically_merged']
ndf['Horizontally_merged'] = new_df['Horizontally_merged']
ndf['Font_selection'] = new_df['Font_selection']
ndf['Is_Formula'] = new_df['Is_Formula']
ndf['Type'] = new_df['Type']
ndf['Font_color'] = new_df['Font_color']
```

```python
r = ndf['Row'].iloc[0]
c = ndf['Column'].iloc[0]
ndf['Row'] -= r
ndf['Column'] -= c
```

```python
ndf["Color"] = pd.factorize(ndf["Color"])[0]
ndf["Type"] = pd.factorize(ndf["Type"])[0]
ndf["Font_color"] = pd.factorize(ndf["Font_color"])[0]
ndf.reset_index(drop= True , inplace= True )
# cont = []
# for i in ndf['Start_content']:
#     a = type(i)
#     if isinstance(i, str) or isinstance(i, datetime) or isinstance(i, time):
#         cont.append(hash(i))
#     else:
#         cont.append(i)
# ndf['Start_content'] = cont
ndf
```

```python
arr = np.empty((ndf.tail(1)['Row'].iloc[0]+1, ndf.tail(1)['Column'].iloc[0]+1), dtype="object")
```

```python
for i, row in ndf.iterrows():
    arr[row['Row'], row['Column']] = row.values.tolist()
```

```python
mass = []
for i in range(len(arr)):
    a = []
    for j in range(len(arr[i])):
        a.extend(arr[i][j])
    mass.append(a)
```

```python
df = pd.DataFrame(data=mass)
df = df.fillna(0)
```

```python
df
```

```python
from sklearn.cluster import AgglomerativeClustering, DBSCAN, OPTICS, KMeans, SpectralClustering
```

```python
df = df[df[0] > 5]
dbs = DBSCAN().fit(df)
df['labels'] = dbs.labels_
first_part_list = df['labels']
df
```

```python
df1 = df[df.labels == -1]
df1 = df1.drop(columns=['labels'])

in_cols = []
for i in df1.columns:
    if int(i)%9 in [2, 3, 4, 5, 6, 7, 8]:
        in_cols.append(True)
    else:
        in_cols.append(False)

df1_ = df1.iloc[:, in_cols]
# df1_ = df1

ald = KMeans(n_clusters=2).fit(df1_)
df1_['labels'] = ald.labels_
df1_['labels'] = df1_['labels'].apply(lambda x: x + 1)
second_part_list = df1_['labels']
df1_
```

```python
for i in second_part_list.index:
    first_part_list[i] = second_part_list[i]
    
to_merge_df = pd.DataFrame()
to_merge_df['Row'] = df[0] + r
to_merge_df['labels'] = first_part_list
```

```python
to_merge_df = to_merge_df.set_index('Row')
to_merge_df
```

```python
str_type_list = []
names = list(new_df.columns)
r_i = names.index('Row') + 1
for row in new_df.itertuples():
    
    a = to_merge_df['labels'][row[r_i]] if row[r_i] in list(to_merge_df.index) else None
    str_type_list.append(a)
str_type_list
```

```python
new_df['row_type'] = str_type_list
new_df['row_type'] = new_df['row_type'].fillna(-1)
new_df
```

```python
new_df.to_csv('processed_tables/2_parsed.csv')
```

```python

```
