from typing import Iterator

import pandas as pd
from overrides import overrides

from structuries.columns import ColumnType
from structuries.document.base import Document
from structuries.fragment import TextFragment
from structuries.structure import StructureNode, DocumentStructure


class TextDocument(Document):


