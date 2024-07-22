import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torch.optim import Adam
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision.models.detection import FasterRCNN
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import ast
import pickle


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
