"""Prompts for working with OCR models."""

# Dots.ocr prompts
DOTS_LAYOUT_PROMPT = """Please output the layout information from this PDF image, including each layout's bbox and its category. The bbox should be in the format [x1, y1, x2, y2]. The layout categories for the PDF document include ['Caption', 'Footnote', 'Formula', 'List-item', 'Page-footer', 'Page-header', 'Picture', 'Section-header', 'Table', 'Text', 'Title']. Do not output the corresponding text. The layout result should be in JSON format."""

DOTS_SYSTEM_PROMPT = "You are a precise document layout analyzer. The input image is exactly {width}x{height} pixels."

# Qwen2.5-VL prompts
QWEN_WORD_DETECTION_SYSTEM_PROMPT = """You are a precise OCR assistant specialized in word detection. Your task is to detect every word in the image and output only a strict JSON list of words with their bounding boxes and confidence scores.

OUTPUT FORMAT (JSON only, no other text):
[
  {
    "word": "exact_word",
    "bbox": [x_min_norm, y_min_norm, x_max_norm, y_max_norm],
    "confidence": 0.X
  },
  ...
]

RULES:
• Output ONLY the JSON array. No explanations, no reasoning, no extra text.
• Coordinates are normalized floats in [0,1] (relative to image width/height).
• Words must be reported in reading order (top to bottom, left to right).
• Omit any non-text elements (logos, lines, noise).
• Confidence must be ≥ 0.05; skip words below this.
• Preserve exact case, punctuation, accents.
• Never include <think>, reasoning, or commentary.
• Output must be valid JSON and nothing else."""

QWEN_WORD_DETECTION_USER_PROMPT = "Detect all text words in the image and return only the JSON array as specified. No explanations."

QWEN_WORD_RECOGNITION_SYSTEM_PROMPT = """You are an OCR specialist. Your task is to transcribe the text from the image exactly as it appears.

OUTPUT FORMAT: Plain text only. No JSON, no markup, no commentary.

RULES:
• Transcribe every visible word in reading order.
• Preserve original spelling, punctuation, line breaks, case, and special characters.
• Do NOT add any explanations, reasoning (e.g., <think>), or formatting.
• Ignore non-text elements (logos, borders, noise).
• Output only the raw transcription.
• Never say 'I think', 'Let me see', or similar phrases.
• Output must be the text only — nothing before or after."""

QWEN_WORD_RECOGNITION_USER_PROMPT = "Transcribe the text from the image exactly. Output only the text. No reasoning, no extra words."


# dots.ocr prompts from GitHub
'''
dict_promptmode_to_prompt = {
    # prompt_layout_all_en: parse all layout info in json format.
    "prompt_layout_all_en": """Please output the layout information from the PDF image, including each layout element's bbox, its category, and the corresponding text content within the bbox.

1. Bbox format: [x1, y1, x2, y2]

2. Layout Categories: The possible categories are ['Caption', 'Footnote', 'Formula', 'List-item', 'Page-footer', 'Page-header', 'Picture', 'Section-header', 'Table', 'Text', 'Title'].

3. Text Extraction & Formatting Rules:
    - Picture: For the 'Picture' category, the text field should be omitted.
    - Formula: Format its text as LaTeX.
    - Table: Format its text as HTML.
    - All Others (Text, Title, etc.): Format their text as Markdown.

4. Constraints:
    - The output text must be the original text from the image, with no translation.
    - All layout elements must be sorted according to human reading order.

5. Final Output: The entire output must be a single JSON object.
""",

    # prompt_layout_only_en: layout detection
    "prompt_layout_only_en": """Please output the layout information from this PDF image, including each layout's bbox and its category. The bbox should be in the format [x1, y1, x2, y2]. The layout categories for the PDF document include ['Caption', 'Footnote', 'Formula', 'List-item', 'Page-footer', 'Page-header', 'Picture', 'Section-header', 'Table', 'Text', 'Title']. Do not output the corresponding text. The layout result should be in JSON format.""",

    # prompt_layout_only_en: parse ocr text except the Page-header and Page-footer
    "prompt_ocr": """Extract the text content from this image.""",

    # prompt_grounding_ocr: extract text content in the given bounding box
    "prompt_grounding_ocr": """Extract text from the given bounding box on the image (format: [x1, y1, x2, y2]).\nBounding Box:\n""",

    # "prompt_table_html": """Convert the table in this image to HTML.""",
    # "prompt_table_latex": """Convert the table in this image to LaTeX.""",
    # "prompt_formula_latex": """Convert the formula in this image to LaTeX.""",
}
'''