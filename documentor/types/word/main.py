import pandas as pd

from documentor.structuries.document import Document, StructuredDocument, StructureNode, Fragment

class SimpleFragment(Fragment):
    data: str = ''
    def __init__(self, row):
        self.data = row

    def __str__(self):
        return self.data


class SimpleDocument(Document):
    data: list[Fragment] = []

    def __init__(self):
        ...
    @classmethod
    def from_df(cls, df: pd.DataFrame):
        ...

    def create_fragments(self, data: list[str]):
        ...

