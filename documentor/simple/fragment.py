from documentor.abstract.document import Fragment
from documentor.semantic.preprocessing.lemmatization import Lemmatizer


class SimpleFragment(Fragment):
    """
    Represents a simple fragment of document

    """
    data: str
    lemmas: list[str]

    def __init__(self, row, *args, **kwargs):
        self.data = row

    def lemmatization(self, *args, **kwargs):
        """
        Lemmatize the text
        :return:
        """
        self.lemmas = Lemmatizer.lemmatize(self.data, args, kwargs)

    def __str__(self, *args, **kwargs):
        """
        Represents a simple fragment of document
        :return:
        """
        return self.data
