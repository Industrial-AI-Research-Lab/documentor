from enum import Enum
from typing import Union, TypeAlias


class DocExtension(str, Enum):
    """
    DocExtension - Enum for file extensions.
    """
    # Text files
    txt = '.txt'
    md = '.md'
    
    # Microsoft Office
    docx = '.docx'
    xls = '.xls'
    xlsx = '.xlsx'
    ppt = '.ppt'
    pptx = '.pptx'
    
    # PDF
    pdf = '.pdf'
    
    # Images
    jpg = '.jpg'
    jpeg = '.jpeg'
    png = '.png'
    
    # Archives
    zip = '.zip'
    seven_z = '.7z'
    
    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def from_string(cls, extension: str) -> 'DocExtension':
        """
        Create an instance of DocExtension from a string.
        
        Args:
            extension (str): File extension (e.g. '.txt', 'txt', or 'TXT')
            
        Returns:
            DocExtension: Corresponding enumeration element
            
        Raises:
            ValueError: If the extension is not supported
        """
        if not extension:
            raise ValueError("Extension cannot be empty")
            
        if not extension.startswith('.'):
            extension = '.' + extension
        extension = extension.lower()
        
        for ext in cls:
            if ext.value == extension:
                return ext
                
        raise ValueError(f"Unsupported extension: {extension}")


# TypeAlias for DocExtension or str - associated with extensions of files
Extension: TypeAlias = Union[DocExtension, str]

ZIP_EXTENSIONS = [DocExtension.zip, DocExtension.seven_z]
