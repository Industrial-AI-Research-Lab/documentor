import ast

import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd
import torch
from sklearn.decomposition import PCA
from torch.optim import Adam
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm

from documentor.formats.excel.parser import SheetParser


class CustomDataset(Dataset):
    """
    Custom dataset for processing annotations and extracting features and targets.

    Attributes:
        annotations (list): List of annotations containing feature and target information.
    """

    def __init__(self, annotations: list):
        """
        Initializes the CustomDataset with the provided annotations.

        Args:
            annotations (list): List of annotations containing feature and target information.
        """
        self.annotations = annotations

    def __len__(self) -> int:
        """
        Returns the number of samples in the dataset.

        Returns:
            int: Number of samples in the dataset.
        """
        return len(self.annotations)

    def __getitem__(self, idx: int):
        """
        Retrieves a sample from the dataset at the given index.

        Args:
            idx (int): Index of the sample to retrieve.

        Returns:
            tuple: A tuple containing the features tensor and the target dictionary.
        """
        # Extract features and convert to tensor
        features = self._apply_pca_to_tensor(
            self._split_and_restructure(torch.tensor(self.annotations[idx]['features'], dtype=torch.float32)))

        # Convert target Excel-style cells to numerical indices
        boxes = [self._convert_target_to_indices(cell) for cell in ast.literal_eval(self.annotations[idx]['target'])]
        labels = torch.ones((len(boxes)), dtype=torch.int64)
        target = {"boxes": torch.tensor(boxes), "labels": labels}

        return features, target

    def _split_and_restructure(self, data: torch.Tensor) -> torch.Tensor:
        """
        Converts a two-dimensional tensor with cell metadata (including row and column indices) into a
        three-dimensional tensor. The first dimension corresponds to the metadata type, and the
        second and third dimensions correspond to row and column positions.

        Args:
            data (torch.Tensor): A two-dimensional tensor where each row includes:
                                 [row index, column index, meta1, meta2, ..., meta12]

        Returns:
            torch.Tensor: A three-dimensional tensor with shape [12, max_row, max_col], where each slice
                          along the first dimension represents one metadata feature arranged according to the cell's row and column.
        """
        max_row = int(torch.max(data[:, 0]).item())
        max_col = int(torch.max(data[:, 1]).item())
        output_tensor = torch.zeros((12, max_row, max_col))

        for entry in data:
            row_idx = int(entry[0].item()) - 1
            col_idx = int(entry[1].item()) - 1
            for i in range(12):
                output_tensor[i, row_idx, col_idx] = entry[i + 2]

        return output_tensor

    def _apply_pca_to_tensor(self, tensor: torch.Tensor) -> torch.Tensor:
        """
        Applies PCA to a tensor to reduce its channel dimension from 12 to 3.

        Args:
            tensor (torch.Tensor): Input tensor of shape [12, x, y] where
                12 is the number of channels,
                x is the number of rows,
                y is the number of columns.

        Returns:
            torch.Tensor: Output tensor of shape [3, x, y] where
                3 is the reduced number of channels.
        """
        if tensor.is_cuda:
            tensor = tensor.cpu()

        original_shape = tensor.shape
        tensor_reshaped = tensor.view(original_shape[0], -1).transpose(0, 1)
        pca = PCA(n_components=3)
        transformed_data = pca.fit_transform(tensor_reshaped.numpy())
        transformed_tensor = torch.tensor(transformed_data, dtype=tensor.dtype).transpose(0, 1)
        final_tensor = transformed_tensor.view(3, original_shape[1], original_shape[2])

        return final_tensor

    def _convert_target_to_indices(self, cell_range: str) -> list:
        """
        Converts an Excel-style cell range (e.g., 'A1:C3') to numerical indices.

        Args:
            cell_range (str): The cell range in Excel format (e.g., 'A1:C3').

        Returns:
            list: A list of four integers representing the start and end rows and columns.
        """

        def _col_to_num(col_str):
            num = 0
            for c in col_str:
                if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    num = num * 26 + (ord(c.upper()) - ord('A')) + 1
            return num

        start_cell, end_cell = cell_range.split(':')
        start_col, start_row = _col_to_num(''.join(filter(str.isalpha, start_cell))), int(
            ''.join(filter(str.isdigit, start_cell)))
        end_col, end_row = _col_to_num(''.join(filter(str.isalpha, end_cell))), int(
            ''.join(filter(str.isdigit, end_cell)))
        return [start_row, start_col, end_row, end_col]


# # TODO add files
# # Load the data from pickle files
# with open('data/train.pkl', 'rb') as f:
#     train = pickle.load(f)
#
# with open('data/test.pkl', 'rb') as f:
#     test = pickle.load(f)
#
# # Initialize CustomDataset instances
# train_dataset = CustomDataset(annotations=train)
# test_dataset = CustomDataset(annotations=test)
#
#
# def load_dataset(dataset: Dataset, batch_size: int, shuffle: bool) -> DataLoader:
#     """
#     Load dataset into a DataLoader.
#
#     Args:
#         dataset (Dataset): The dataset to load.
#         batch_size (int): The number of samples per batch.
#         shuffle (bool): Whether to shuffle the data at every epoch.
#
#     Returns:
#         DataLoader: DataLoader for the given dataset.
#     """
#     data_loader = DataLoader(dataset,
#                              batch_size=batch_size,
#                              shuffle=shuffle,
#                              pin_memory=True if torch.cuda.is_available() else False)
#     return data_loader
#
#
# # Calculate the train/validation split sizes
# train_size = int(0.8 * len(train_dataset))
# val_size = len(train_dataset) - train_size
#
# # Split the dataset into training and validation sets
# train_dataset, val_dataset = random_split(train_dataset, [train_size, val_size],
#                                           generator=torch.Generator().manual_seed(42))
#
# # Load the datasets into DataLoaders
# train_loader = load_dataset(train_dataset, batch_size=1, shuffle=True)
# val_loader = load_dataset(val_dataset, batch_size=1, shuffle=False)
# test_loader = load_dataset(test_dataset, batch_size=1, shuffle=False)


class TableDetectionModel:
    """
    A class for table detection model that includes methods for training, validation, and testing.

    Attributes:
        model (torch.nn.Module): The table detection model.
        device (torch.device): The device for computation (CPU or GPU).
        iou_threshold (float): The threshold for Intersection over Union (IoU) to calculate accuracy.
        optimizer (torch.optim.Optimizer): The optimizer for training the model.
        losses_per_epoch (list): List to store the loss value for each epoch.
        accuracy_per_epoch (list): List to store the accuracy value for each epoch.
        validation_losses_per_epoch (list): List to store the validation loss value for each epoch.
        validation_accuracy_per_epoch (list): List to store the validation accuracy value for each epoch.
    """

    def __init__(self, model: torch.nn.Module, device: torch.device, iou_threshold: float = 0.1,
                 learning_rate: float = 0.0005, weight_decay: float = 5e-4):
        """
        Initializes the TableDetectionModel.

        Args:
            model (torch.nn.Module): The table detection model.
            device (torch.device): The device for computation (CPU or GPU).
            iou_threshold (float): The threshold for Intersection over Union (IoU) to calculate accuracy.
            learning_rate (float): The learning rate for the optimizer.
            weight_decay (float): The weight decay for the optimizer.
        """
        self.model = model
        self.device = device
        self.iou_threshold = iou_threshold
        self.optimizer = Adam([p for p in model.parameters() if p.requires_grad], lr=learning_rate,
                              weight_decay=weight_decay)
        self.losses_per_epoch = []
        self.accuracy_per_epoch = []
        self.validation_losses_per_epoch = []
        self.validation_accuracy_per_epoch = []

    @staticmethod
    def calculate_iou(box1: torch.Tensor, box2: torch.Tensor) -> float:
        """
        Calculate the Intersection over Union (IoU) of two bounding boxes.

        Args:
            box1 (torch.Tensor): The first bounding box.
            box2 (torch.Tensor): The second bounding box.

        Returns:
            float: The IoU value.
        """
        x1 = torch.max(box1[0], box2[0])
        y1 = torch.max(box1[1], box2[1])
        x2 = torch.min(box1[2], box2[2])
        y2 = torch.min(box1[3], box2[3])

        intersection = (x2 - x1).clamp(0) * (y2 - y1).clamp(0)
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        union = area1 + area2 - intersection

        return intersection / union

    def calculate_accuracy(self, data_loader: DataLoader) -> float:
        """
        Calculate the accuracy of the model on the given data loader.

        Args:
            data_loader (DataLoader): The data loader with the data to evaluate.

        Returns:
            float: The accuracy of the model.
        """
        self.model.eval()
        total_correct = 0
        total_samples = 0

        with torch.no_grad():
            for data in tqdm(data_loader):
                try:
                    documents = []
                    targets = []
                    for feature, target in data:
                        documents.append(feature.to(self.device))
                        targ = {}
                        targ['boxes'] = target["boxes"].to(self.device)
                        targ['labels'] = target["labels"].to(self.device)
                        targets.append(targ)

                    outputs = self.model(documents)
                    for output, target in zip(outputs, targets):
                        pred_boxes = output['boxes']
                        pred_labels = output['labels']
                        true_boxes = target['boxes']
                        true_labels = target['labels']

                        for i in range(len(true_boxes)):
                            iou_scores = [self.calculate_iou(true_boxes[i], pred_box) for pred_box in pred_boxes]
                            if iou_scores:
                                max_iou, max_idx = torch.max(torch.tensor(iou_scores), 0)
                            else:
                                max_iou, max_idx = 0, 0
                            if max_iou >= self.iou_threshold and pred_labels[max_idx] == true_labels[i]:
                                total_correct += 1

                        total_samples += len(true_boxes)

                except Exception as e:
                    print(f'Error: {e}')
                    continue

        accuracy = total_correct / total_samples
        return accuracy

    @staticmethod
    def detection_by_heuristic(sheet, data):
        """
       Detects tables in the given sheet using heuristic methods.

       Args:
           sheet (openpyxl.worksheet.worksheet.Worksheet): The sheet to detect tables in.
           data (Any): Additional data for detection.

       Returns:
           list: A list of table boundaries (start_row, start_col, end_row, end_col).
       """

        def is_row_empty(row):
            for cell in row:
                value = cell.value
                left = cell.border.left.style if cell.border.left.style else None
                right = cell.border.right.style if cell.border.right.style else None

                if any(item is not None for item in [value, left, right]):
                    return False
            return True

        def is_column_empty(table, column_index):
            for row in table:
                value = row[column_index].value
                top = row[column_index].border.top.style if row[column_index].border.top.style else None
                bottom = row[column_index].border.bottom.style if row[column_index].border.bottom.style else None

                if any(item is not None for item in [value, top, bottom]):
                    return False
            return True

        def split_table_by_empty_columns(table):
            subtables = []
            current_subtable = []
            columns_count = len(table[0])

            for end_col in range(columns_count):
                if is_column_empty(table, end_col):
                    if current_subtable:
                        subtables.append(current_subtable)
                        current_subtable = []
                else:
                    for row_index, row in enumerate(table):
                        if len(current_subtable) <= row_index:
                            current_subtable.append([])
                        current_subtable[row_index].append(row[end_col])

            if current_subtable:
                subtables.append(current_subtable)

            return subtables

        def get_table_bounds(table):
            model = data
            start_row = table[0][0].row
            start_col = table[0][0].column
            end_row = table[-1][0].row
            end_col = table[0][-1].column
            return (start_row, start_col, end_row, end_col)

        def is_valid_table(table):
            if len(table) == 0 or len(table[0]) == 0:
                return False
            if len(table) == 1 or len(table[0]) == 1:
                return False
            for row in table:
                for cell in row:
                    if cell.border.left.style or cell.border.right.style or cell.border.top.style or cell.border.bottom.style:
                        return True
            return False

        tables = []
        current_table = []
        for row in sheet.iter_rows():
            if is_row_empty(row):
                if current_table:
                    subtables = split_table_by_empty_columns(current_table)
                    valid_subtables = [table for table in subtables if is_valid_table(table)]
                    tables.extend(valid_subtables)
                    current_table = []
            else:
                current_table.append(row)

        if current_table:
            subtables = split_table_by_empty_columns(current_table)
            valid_subtables = [table for table in subtables if is_valid_table(table)]
            tables.extend(valid_subtables)

        table_bounds = [get_table_bounds(table) for table in tables]

        return table_bounds

    def predict(self, path: str, sheet_name: str) -> list:
        """
        Predict table boundaries in a specified Excel sheet.

        This method combines machine learning-based predictions using the trained model
        with heuristic-based detection to determine the boundaries of tables within the given Excel sheet.

        Args:
            path (str): The file path of the Excel workbook.
            sheet_name (str): The name of the sheet within the workbook where table detection is to be performed.

        Returns:
            list: A list of tuples, where each tuple represents the boundaries of a detected table.
                  Each tuple contains four integers: (start_row, start_col, end_row, end_col),
                  indicating the starting row and column, as well as the ending row and column of the table.
        """

        sheet_parser = SheetParser()
        doc = sheet_parser.parse_file(path=path, sheet_name=sheet_name)

        df = doc.to_df()
        df["is_empty"] = np.where(df["type"] == "NoneType", 1, 0)
        df["color"] = pd.factorize(df["color"])[0]
        df["font_color"] = pd.factorize(df["font_color"])[0]
        df.drop(columns=['value', 'start_content', 'relative_id', 'type'], inplace=True)
        df_dict = df.to_dict('index')

        features = [tuple(val.values()) for val in df_dict.values()]

        self.model.eval()
        outputs = self.model(features)

        wb = openpyxl.load_workbook(path)
        sheet = wb[sheet_name]
        new_output = self.detection_by_heuristic(sheet, outputs)
        return new_output

    def save_model(self, epoch: int, path: str = "model_checkpoint.pth"):
        """
        Saves the model state to a file after each epoch.

        Args:
            epoch (int): The current epoch.
            path (str): The path to save the model file.
        """
        torch.save({
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'losses_per_epoch': self.losses_per_epoch,
            'accuracy_per_epoch': self.accuracy_per_epoch,
            'validation_losses_per_epoch': self.validation_losses_per_epoch,
            'validation_accuracy_per_epoch': self.validation_accuracy_per_epoch,
        }, path)
        print(f"Model checkpoint saved at epoch {epoch}")

    def load_model(self, path: str):
        """
        Loads the model state from a file.

        Args:
            path (str): The path to load the model file from.
        """
        checkpoint = torch.load(path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.losses_per_epoch = checkpoint['losses_per_epoch']
        self.accuracy_per_epoch = checkpoint['accuracy_per_epoch']
        self.validation_losses_per_epoch = checkpoint['validation_losses_per_epoch']
        self.validation_accuracy_per_epoch = checkpoint['validation_accuracy_per_epoch']
        print(f"Model loaded from {path}")

    def train(self, train_data_loader: DataLoader, validation_data_loader: DataLoader, num_epochs: int = 5):
        """
        Train the model and calculate accuracy on the validation set.

        Args:
            train_data_loader (DataLoader): The data loader with training data.
            validation_data_loader (DataLoader): The data loader with validation data.
            num_epochs (int): The number of epochs to train.
        """
        for epoch in tqdm(range(num_epochs)):
            i = 0
            total_loss = 0
            self.model.train()
            for data in tqdm(train_data_loader):
                try:
                    documents = []
                    targets = []
                    for feature, target in data:
                        documents.append(feature.to(self.device))
                        targ = {}
                        targ['boxes'] = target["boxes"].to(self.device)
                        targ['labels'] = target["labels"].to(self.device)
                        targets.append(targ)

                    loss_dict = self.model(documents, targets)
                    losses = sum(loss for loss in loss_dict.values())

                    self.optimizer.zero_grad()
                    losses.backward()
                    self.optimizer.step()

                    total_loss += losses.item()

                except Exception as e:
                    print(f'Error: {e}')
                    continue

            avg_loss = total_loss / (i + 1)
            self.losses_per_epoch.append(avg_loss)
            print(f'Epoch {epoch}, Average Loss: {avg_loss}')

            # Evaluate accuracy on the validation data
            accuracy = self.calculate_accuracy(validation_data_loader)
            self.accuracy_per_epoch.append(accuracy)
            print(f'Epoch {epoch}, Accuracy: {accuracy}')

            self.save_model(epoch, path="data/model_checkpoint.pth")

    def test(self, test_data_loader: DataLoader) -> float:
        """
        Test the model on the test set.

        Args:
            test_data_loader (DataLoader): The data loader with test data.

        Returns:
            float: The accuracy on the test set.
        """
        self.model.eval()
        accuracy = self.calculate_accuracy(test_data_loader)
        return accuracy

    def plot_metrics(self):
        """
        Plot the loss and accuracy metrics over epochs.
        """
        plt.figure(figsize=(12, 5))

        # Loss plot
        plt.subplot(1, 2, 1)
        plt.plot(range(len(self.losses_per_epoch)), self.losses_per_epoch, label='Training Loss')
        plt.plot(range(len(self.validation_losses_per_epoch)), self.validation_losses_per_epoch,
                 label='Validation Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.title('Loss per Epoch')
        plt.legend()

        # Accuracy plot
        plt.subplot(1, 2, 2)
        plt.plot(range(len(self.accuracy_per_epoch)), self.accuracy_per_epoch, label='Training Accuracy')
        plt.plot(range(len(self.validation_accuracy_per_epoch)), self.validation_accuracy_per_epoch,
                 label='Validation Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.title('Accuracy per Epoch')
        plt.legend()

        plt.show()
