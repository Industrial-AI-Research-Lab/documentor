from structuries.document.base import Document


class SheetDocument(Document):
    """
    Document type representing spreadsheets (e.g., Excel workbooks).

    Attributes:
        pages_names: Names of sheets (tabs) in the workbook.
    """
    pages_names: list[str]