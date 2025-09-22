from structuries.document.base import Document


class SheetDocument(Document):
    """
    Document type representing spreadsheets (e.g., Excel workbooks).

    Attributes:
        pages_names: Names of sheets (tabs) in the workbook.
    """
    pages_names: list[str]

    def __init__(self, pages_names: list[str], **kwargs):
        super().__init__(**kwargs)
        self.pages_names = pages_names
