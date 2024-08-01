from .lang_models.base import BaseLLMWrapper
from .preprocessing.base import BaseSemanticModel
from documentor.structuries.document import Document


class Pipeline:
    """
    A sequence of semantic models for text preprocessing

    """

    def __init__(self, steps: list[tuple[str, BaseSemanticModel | BaseLLMWrapper]], *args, **kwargs):
        self.steps = steps

    def estimate(self, document: Document, **kwargs):
        """
        Run a pipeline with data from document
        :param document:
        :return:
        """
        for step in self.steps:
            step[1].estimate(document, **kwargs)

        return document.copy()



