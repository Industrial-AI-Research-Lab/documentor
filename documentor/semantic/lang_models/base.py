from abc import ABC, abstractmethod


class BaseLLMWrapper(ABC):
    """
    Base class for llm wrapping.

    """

    @abstractmethod
    def prompt(self, prompt, **kwargs):
        ...
