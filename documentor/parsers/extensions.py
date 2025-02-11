from enum import Enum
from typing import Union, TypeAlias


class DocExtension(str, Enum):
    """
    DocExtension - Enum class for parser file extensions.
    """
    docx = 'docx'
    doc = 'doc'
    pdf = 'pdf'
    xls = 'xls'
    xlsx = 'xlsx'
    odt = 'odt'
    rtf = 'rtf'
    md = 'md'
    zip = 'zip'
    seven_z = '7z'
    txt = 'txt'
    not_supported = 'not_supported'

    def __init__(self, value: str):
        self.value = value.lower()


# TypeAlias for DocExtension or str - associated with extensions of files
Extension: TypeAlias = Union[DocExtension, str]

ZIP_EXTENSIONS = [DocExtension.zip, DocExtension.seven_z]
