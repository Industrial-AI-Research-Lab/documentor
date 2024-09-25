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
from documentor.types.excel_detection import TableDetectionModel
```

Initialize the class for table detection.
- To run the model, download the file with the [model weights](https://niuitmo-my.sharepoint.com/:u:/g/personal/mr_basilaev_niuitmo_ru/EcVrp0_Lcx1AgGBmg5BKmoMBn1dlA-MQx40NhDzzvGGbUg?e=uuecqN)

```python
table_detection_model.load_model("model_checkpoint.pth")
```

Predict the table boundaries
```python
predicted_boundaries = table_detection_model.predict(path='data/Global_Hot_List.xlsx', 
                                                     sheet_name='Hotlist - Identified ')
```

Output the predicted table boundaries
```python
for bounds in predicted_boundaries:
    print(f"Table bounds: Start Row: {bounds[0]}, Start Col: {bounds[1]}, "
          f"End Row: {bounds[2]}, End Col: {bounds[3]}")
```