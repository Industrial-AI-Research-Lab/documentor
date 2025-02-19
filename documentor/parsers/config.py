from enum import Enum


class ParsingSchema(Enum):
    """
    The class provides a way to specify the parsing schema.
    """
    paragraphs = 'paragraphs'
    lines = 'lines'
    chapters = 'chapters'
    characters = 'characters'
    pages = 'pages'
    full = 'full'


class ParsingConfig:
    """
    The class provides a way to configure the parsing process.

    Attributes:
        parsing_schema (ParsingSchema): the parsing schema to be used.
        parsing_batch_size (int): the size of the batch to be parsed.
        extract_images (bool): whether to extract images from the document.
        extract_tables (bool): whether to extract tables from the document.
        extract_formulas (bool): whether to extract formulas from the document.
    """

    def __init__(
            self,
            parsing_schema: ParsingSchema = ParsingSchema.lines,
            parsing_batch_size: int = 1,
            extract_images: bool = False,
            extract_tables: bool = False,
            extract_formulas: bool = False,
    ):
        """
        The class constructor.

        Args:
            parsing_schema (ParsingSchema): the parsing schema to be used.
            parsing_batch_size (int): the size of elems from ParsingSchema in each Document. Scheduled be positive.
            extract_images (bool): whether to extract images from the document.
            extract_tables (bool): whether to extract tables from the document.
            extract_formulas (bool): whether to extract formulas from the document.
        """
        self.parsing_schema = parsing_schema
        if parsing_batch_size < 1:
            raise ValueError('The batch size must be at least one')
        self.parsing_batch_size = parsing_batch_size
        self.extract_images = extract_images
        self.extract_tables = extract_tables
        self.extract_formulas = extract_formulas
