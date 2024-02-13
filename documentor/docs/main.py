import pandas as pd

from documentor.structuries.document import TextDocument, StructuredDocument, StructureNode
from documentor.text.fragment import TextFragment


class SimpleFragment(TextFragment):
    data: str = ''
    def __init__(self, row):
        self.data = row

    def __str__(self):
        return self.data


class SimpleDocument(TextDocument):
    data: list[TextFragment] = []

    def __init__(self):
        ...
    @classmethod
    def from_df(cls, df: pd.DataFrame):
        ...

    def create_fragments(self, data: list[str]):
        ...

