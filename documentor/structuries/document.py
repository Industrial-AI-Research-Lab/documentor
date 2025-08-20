from abc import ABC, abstractmethod
from typing import Iterator

import pandas as pd
from overrides import overrides

from documentor.structuries.columns import ColumnType
from documentor.structuries.fragment import Fragment

from documentor.structuries.structure import StructureNode, DocumentStructure
from documentor.structuries.type_check import TypeChecker as tc


class DocumentInterface(ABC):
    """
    Interface for document with fragments.
    """

    @abstractmethod
    def build_fragments(self) -> list[Fragment]:
        """
        List of fragments of the Document.

        Note:
            If speed is important, prefer using iter_rows().

        Returns:
            list[Fragment]: List of fragments.
        """
        pass

    @abstractmethod
    def iter_rows(self) -> Iterator[tuple[int, pd.Series]]:
        """
        Iterate over all fragments of the Document.

        Returns:
            Iterator[tuple[int, pd.Series]]: Iterator over (row_index, row) pairs.
        """
        pass

    @abstractmethod
    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame with data about fragments.
        """
        pass


class Document(DocumentInterface):
    """
    Simple realization of document with string fragments.

    Document is a collection of fragments. Otherwise, document does not store fragments, it works with pd.DataFrame,
    which contain same column names as Fragment class field names.
    """
    _data: pd.DataFrame
    _columns: dict[str, ColumnType] = {field: ColumnType(type) for field, type in Fragment.param_types_dict().items()}
    _root: StructureNode | None = None
    _structure: DocumentStructure | None = None

    def __init__(self, data: pd.DataFrame):
        """
        Initialize a Document from a pandas DataFrame.

        Args:
            data (pd.DataFrame): DataFrame containing columns corresponding to Fragment fields.

        Notes:
            Required columns:
                - value: Value of the fragment.
            Optional columns used for initialization:
                - ground_truth: Ground truth label of the fragment if it is labeled.
                - label: Label of the fragment from classification.
                - vector: Vector representation of the fragment.
                - tokens: List of tokens of the fragment.
                - token_vectors: List of vectors of tokens of the fragment.
        """
        tc.check_data_frame_type(data)
        # tc.check_data_frame_columns(data, self._columns)
        columns = list[self._columns.keys()]
        self._data = data[columns].copy()

    @overrides
    def build_fragments(self) -> list[Fragment]:
        """
        List of fragments of the Document.

        Note:
            If speed is important, prefer using iter_rows().

        Returns:
            list[Fragment]: List of fragments.
        """
        return [Fragment(**row.to_dict()) for _, row in self._data.iterrows()]

    @overrides
    def iter_rows(self) -> Iterator[tuple[int, pd.Series]]:
        """
        Iterate over all fragments of the Document with their row numbers.

        Returns:
            Iterator[tuple[int, pd.Series]]: Iterator over (row_index, row) pairs.
        """
        for i, row in self._data.iterrows():
            yield i, row

    @overrides
    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame with data about fragments.
        """
        return self._data.copy()

    @property
    def value(self) -> pd.Series:
        """
        Values of all fragments.

        Returns:
            pd.Series: All values.
        """
        return self._data['value']

    @property
    def ground_truth(self) -> pd.Series:
        """
        Ground truth labels of all fragments.

        Returns:
            pd.Series: All ground truth labels.
        """
        return self._data['ground_truth']

    @property
    def label(self) -> pd.Series:
        """
        Labels of all fragments.

        Returns:
            pd.Series: All labels.
        """
        return self._data['label']

    @label.setter
    def label(self, value: pd.Series) -> None:
        """
        Set labels of all fragments.

        Args:
            value (pd.Series): New labels.

        Raises:
            TypeError: If value.dtype is not the same as Fragment.label type.
        """
        # tc.check_series(value, self._columns['label'])
        self._data['label'] = value

    @property
    def vector(self) -> pd.Series:
        """
        Vector representations of all fragments.

        Returns:
            pd.Series: All vector representations.
        """
        return self._data['vector']

    @vector.setter
    def vector(self, value: pd.Series) -> None:
        """
        Set vector representations of all fragments.

        Args:
            value (pd.Series): New vector representations.

        Raises:
            TypeError: If value.dtype is not the same as Fragment.vector type.
        """
        # tc.check_series(value, self._columns['vector'])
        self._data['vector'] = value

    @property
    def tokens(self) -> pd.Series:
        """
        Tokens of all fragments.

        Returns:
            pd.Series: All tokens.
        """
        return self._data['tokens']

    @tokens.setter
    def tokens(self, value: pd.Series) -> None:
        """
        Set tokens of all fragments.

        Args:
            value (pd.Series): New tokens.

        Raises:
            TypeError: If value.dtype is not the same as Fragment.tokens type.
        """
        # tc.check_series(value, self._columns['tokens'])
        self._data['tokens'] = value

    @property
    def token_vectors(self) -> pd.Series:
        """
        Vectors of tokens of all fragments.

        Returns:
            pd.Series: All token vectors.
        """
        return self._data['token_vectors']

    @token_vectors.setter
    def token_vectors(self, value: pd.Series) -> None:
        """
        Set vectors of tokens of all fragments.

        Args:
            value (pd.Series): New token vectors.

        Raises:
            TypeError: If value.dtype is not the same as Fragment.token_vectors type.
        """
        # tc.check_series(value, self._columns['token_vectors'])
        self._data['token_vectors'] = value

    def copy(self):
        ...
