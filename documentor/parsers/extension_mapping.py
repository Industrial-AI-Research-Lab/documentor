from copy import deepcopy

from documentor.parsers.base import BaseBlobParser
from documentor.parsers.extensions import DocExtension, Extension
from parsers.txt.base import TextBlobParser
from parsers.excel.base import ExcelBlobParser


class ExtensionMapping:
    """
    ExtensionMapping - Class for mapping file extensions to parsers.
    Attributes:
        _ext2parser (dict[Extension, BaseBlobParser]): A dictionary mapping file extensions to parsers.
    """
    _ext2parser: dict[Extension, BaseBlobParser]

    def __init__(self, ext2parser: dict[Extension, BaseBlobParser] | None = None):
        """
        Initialize the ExtensionMapping. By default, init all Documentor's parsers.
        Args:
            ext2parser (dict[Extension, BaseBlobParser]): A dictionary mapping file extensions to parsers.
                Defaults to None.
        """
        if ext2parser is None:
            ext2parser = {
                DocExtension.txt: TextBlobParser(),
                DocExtension.xlsx: ExcelBlobParser(),
                DocExtension.xls: ExcelBlobParser(),
            }
        self._ext2parser = deepcopy(ext2parser)

    def get_parser(self, extension: Extension) -> BaseBlobParser:
        """
        Get the parser associated with the given extension.
        Args:
            extension (Extension): The extension to get the parser for.
        """
        if not self.is_valid_extension(extension):
            raise ValueError(f"No parser found for extension {extension}")
        return self._ext2parser[extension]

    def is_valid_extension(self, extension: Extension) -> bool:
        """
        Check if the extension is valid.
        Args:
            extension (Extension): The extension to check.
        """
        return extension in self._ext2parser
