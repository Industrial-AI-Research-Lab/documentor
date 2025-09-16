"""Category mapping for dots.ocr to Fragment types."""

from documentor.structuries.fragment import (
    CaptionFragment,
    FootnoteFragment,
    ListItemFragment,
    PageHeaderFragment,
    PageFooterFragment,
    ImageFragment,
    HeaderFragment,
    TableFragment,
    ParagraphFragment,
    TitleFragment,
    LatexFormulaFragment,
)

# Mapping of dots.ocr categories to Fragment types
DOTS_CATEGORY_MAPPING = {
    'Caption': CaptionFragment,
    'Footnote': FootnoteFragment,
    'List-item': ListItemFragment,
    'Page-header': PageHeaderFragment,
    'Page-footer': PageFooterFragment,
    'Picture': ImageFragment,
    'Section-header': HeaderFragment,
    'Table': TableFragment,
    'Text': ParagraphFragment,
    'Title': TitleFragment,
    'Formula': LatexFormulaFragment,
}

# Reverse mapping for logging
FRAGMENT_TO_CATEGORY = {v: k for k, v in DOTS_CATEGORY_MAPPING.items()}