from documentor.abstract.document import Fragment


class SimpleFragment(Fragment):
    """
    Represents a simple fragment of document

    """
    data: str = ''
    def __init__(self, row):
        self.data = row

    def __str__(self):
        return self.data
