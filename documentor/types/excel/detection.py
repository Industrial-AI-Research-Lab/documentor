import numpy as np
import torch
import torch.nn as nn
import torchvision
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.rpn import AnchorGenerator
from torch.optim import SGD
from torch.utils.data import DataLoader
import pandas as pd
import json

from tqdm import tqdm

from documentor.types.excel.parser import SheetParser
from xls2xlsx import XLS2XLSX

import os
from pathlib import Path

train = []
test = []
annotation = pd.read_csv(r"C:\Users\Danny\Desktop\IAI\data\tables_annotation.csv")
for index, row in tqdm(annotation.iterrows()):

    try:
        path = rf'C:\Users\Danny\Desktop\IAI\data\{row["path"]}\{row["Name"]}'
        sheet_name = row['Sheet']
        sheet_parser = SheetParser()
        doc = sheet_parser.parse_file(path=path, sheet_name=sheet_name)
        sheet_parser.to_csv(doc, rf'C:\Users\Danny\Desktop\IAI\data\parse_dataset\{row["Name"][:-4]}csv')

        df = doc.to_df()
        df["is_empty"] = np.where(df["type"] == "NoneType", 1, 0)
        df["color"] = pd.factorize(df["color"])[0]
        df["font_color"] = pd.factorize(df["font_color"])[0]
        df.drop(columns=['value', 'start_content', 'relative_id', 'type'], inplace=True)
        df_dict = df.to_dict('index')

        features = [tuple(val.values()) for val in df_dict.values()]
        target_tables = row['tables']

        if row['train/test'] == 'training_set':
            train.append(dict(features=features, target=target_tables))
        else:
            test.append(dict(features=features, target=target_tables))

        sheet_parser.to_csv(doc, rf'C:\Users\Danny\Desktop\IAI\data\parse_dataset\{row["Name"][:-4]}csv')
        with open(r'C:\Users\Danny\Desktop\IAI\data\train.json', 'w') as file:
            json.dump(train, file)
        with open(r'C:\Users\Danny\Desktop\IAI\data\test.json', 'w') as file:
            json.dump(test, file)
    except Exception:
        continue

#
# # Загрузка предобученной модели на датасете COCO и настройка количества классов (фон + таблица)
# def create_model(num_classes):
#     # Загрузка предобученной модели ResNet50, которая будет использоваться как backbone
#     backbone = torchvision.models.resnet50(pretrained=True)
#     # Удаление слоя классификации на последнем слое
#     backbone = nn.Sequential(*list(backbone.children())[:-2])
#
#     # RPN (Region Proposal Network) генерирует предложения регионов для детектирования
#     anchor_generator = AnchorGenerator(sizes=((32, 64, 128, 256, 512),),
#                                        aspect_ratios=((0.5, 1.0, 2.0),))
#
#     # Определение размера выходных данных для RoI Pooling
#     roi_pooler = torchvision.ops.MultiScaleRoIAlign(featmap_names=['0'],
#                                                     output_size=7,
#                                                     sampling_ratio=2)
#
#     # Собираем модель Faster R-CNN
#     model = FasterRCNN(backbone,
#                        num_classes=num_classes,
#                        rpn_anchor_generator=anchor_generator,
#                        box_roi_pool=roi_pooler)
#
#     return model
#
#
# # Создание модели с двумя классами (0 - фон, 1 - таблица)
# model = create_model(num_classes=2)
#
# # Предполагается, что train_data_loader уже определен
# train_data_loader = DataLoader(...)  # Заполните своим DataLoader для обучающего набора
#
# device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
#
# # Перемещаем модель на доступное устройство
# model.to(device)
#
# # Оптимизатор
# params = [p for p in model.parameters() if p.requires_grad]
# optimizer = SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
#
# # Цикл обучения
# num_epochs = 10
#
# for epoch in range(num_epochs):
#     model.train()
#     i = 0
#     for images, targets in train_data_loader:
#         images = list(image.to(device) for image in images)
#         targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
#
#         loss_dict = model(images, targets)
#
#         losses = sum(loss for loss in loss_dict.values())
#
#         optimizer.zero_grad()
#         losses.backward()
#         optimizer.step()
#
#         if i % 50 == 0:
#             print(f'Epoch: {epoch}, Iteration: {i}, Loss: {losses.item()}')
#         i += 1
