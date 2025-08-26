"""
Descriptions for fragment types, intended for use by LLMs and heuristics.

Each constant is a multi-line guidance string describing how to identify a region type.
"""
IMAGE = """
A contiguous page area that primarily contains visual content rather than running body text. Includes photographs, drawings, diagrams, charts/plots, maps, flowcharts, infographics, screenshots, and pictograms. May appear grayscale or color, with continuous-tone textures (photos/halftones) or line art (sharp strokes, vector-like edges).
Visual/structural cues (positive):
Often rectangular; may have a thin border, drop shadow, or clear whitespace margins; can be full-bleed across one or multiple columns.
Low paragraph-text density inside the region; if text exists, it is sparse and functional (axis labels, legends, short callouts).
Adjacent caption block above or below; common caption tokens and their variants: "Figure", "Fig.", "Image", "Illustration", "Plate".
Multilingual caption tokens (non-exhaustive):
- Russian: "Рис.", "Изображение", "Иллюстрация"
- Chinese (简体): "图", "插图", "图表"
- Spanish: "Figura", "Imagen", "Ilustración"
- Arabic: "شكل", "صورة"
- French: "Figure", "Illustration", "Image", "Planche"
- German: "Abb.", "Abbildung", "Bild"
- Portuguese: "Figura", "Imagem", "Ilustração"
- Hindi: "आकृति", "चित्र", "चित्रण"
Surrounding layout shows interruption of normal text flow: wrap-around text, column break, or centered placement.
Texture statistics differ from body text: larger connected components, broader edge orientations, and non-grid patterns.
Exclusions (negative cues):
Tables (regular gridlines, repeated cell structure, dense alphanumeric content).
Mathematical blocks/equations and code listings (dense glyph clusters with consistent line baselines).
Headers/footers, page numbers, footnotes, watermarks, stamps, signatures, barcodes/QR (unless explicitly cataloged as figures).
Decorative lines or horizontal rules without substantive visual content.
Edge cases to still count as images:
Multi-panel figures labeled (a), (b), (c) within one bounding area.
Diagrams with heavy labeling, legends, or arrows, provided running text is not dominant.
Rotated or skewed figures; broken or partial borders; halftone/moire patterns from scanning.
Boundary preference:
Include the entire visual region and, when present, the immediately attached caption block; exclude unrelated surrounding paragraph text.
"""

TABLE = """
Object: "Table region" on a scanned document page
A contiguous area presenting data in a row–column structure (with or without visible ruling). Usually accompanied by a title/caption ("Table", "Tab.") and optional footnotes.
Multilingual caption tokens (non-exhaustive):
- Russian: "Таблица", "Табл."
- Chinese (简体): "表", "表格"
- Spanish: "Tabla"
- Arabic: "جدول"
- French: "Tableau"
- German: "Tabelle"
- Portuguese: "Tabela"
- Hindi: "तालिका"
Visual/structural cues (positive):
Grid-like layout: repeated alignment of text blocks into columns and rows; strong vertical/horizontal edge frequency (even when lines are invisible).
Presence of ruling (full/partial gridlines), cell borders, or whitespace gutters forming implicit cells; uniform row height or column widths.
Header row/column often emphasized (bold, ALL CAPS, shading, or thicker rule).
High density of short tokens: numbers, units, abbreviations, ±, %, currency symbols; decimal alignment; column headers.
Surrounding caption/notes (e.g., "Note: …", superscripts *, †, ‡) above or below the grid.
Exclusions (negative cues):
Paragraph text columns without row–column intersections (no consistent cell structure, hyphenation across lines).
Code blocks/math arrays rendered as text; figure legends; forms with free-text lines when not arranged in a data grid.
Calendars or multi-column lists unless cells clearly form a consistent table.
Edge cases to still count as tables:
Borderless tables built with whitespace alignment only.
Merged cells, multi-level headers, stub columns, rotated header text, or wrapped multi-line cells.
Split tables that continue across pages/columns (treat each visible segment as a table region; link via caption/continuation markers if available).
Boundary preference:
Include the entire grid area plus immediately attached caption/title and footnotes if clearly tied to the table; exclude unrelated surrounding paragraphs.
"""

PARAGRAPH = """
Object: "Text paragraph region" on a scanned document page
A contiguous block of running prose forming one logical paragraph within a column or page.
Visual/structural cues (positive):
Multiple consecutive lines with consistent baseline spacing and uniform left/right text margins; typical paragraph width equals the enclosing column.
First-line indent or spacing before/after the block; justified or ragged-right alignment with natural word spacing.
Presence of sentence punctuation (.?!;), hyphenation at line ends, mixed-case words; font size smaller than headings.
No persistent vertical alignment across multiple columns (unlike tables).
Exclusions (negative cues):
Bulleted/numbered lists (leading bullets/dashes/Arabic or Roman numerals per line).
Captions (short lines adjacent to figures/tables, often beginning with tokens like "Figure"/"Fig."/"Table" or multilingual variants):
- Russian: "Рис.", "Таблица"/"Табл."
- Chinese (简体): "图"/"图表", "表"/"表格"
- Spanish: "Figura", "Tabla"
- Arabic: "شكل", "جدول"
- French: "Figure", "Tableau"
- German: "Abb."/"Abbildung", "Tabelle"
- Portuguese: "Figura", "Tabela"
- Hindi: "आकृति", "तालिका"
Code blocks, equations, footers/headers, page numbers, marginalia.
Forms and key–value pairs arranged in two columns (likely tables or metadata blocks).
Edge cases to still count as paragraphs:
Paragraphs with inline math, citations [1], or occasional bold/italic words.
Slight skew/rotation or minor line curvature due to scanning.
Single-sentence paragraphs (e.g., abstracts' lead-in sentences) if spacing/indent matches paragraph style.
Boundary preference:
Include from the first to last line that shares the paragraph's vertical spacing and left/right alignment; exclude leading section titles and trailing captions not styled as part of the paragraph.
"""

TITLE = """
Object: "Heading / Title region" on a scanned document page
A short line (or small block) of display text that names a document, section, or subsection.
Visual/structural cues (positive):
Font size larger than body text and/or increased weight (bold), small caps, or distinctive typeface; often centered or left-aligned with extra whitespace above/below.
Numbering patterns: "1", "1.1", "A.", "I.", "Chapter 3", "Section 2", "Appendix A"; optional trailing colon.
Case/typography cues: Title Case, ALL CAPS, or small caps; no end-of-line hyphenation.
Positioned at the top of a page/column or immediately preceding a paragraph; may include decorative rules above/below.
Common heading tokens across major languages (non-exhaustive):
- English: "Abstract", "Introduction", "Methods", "Results", "Conclusion(s)", "References"
- Russian: "Аннотация", "Введение", "Методы/Методика", "Результаты", "Заключение", "Литература/Ссылки"
- Chinese (简体): "摘要", "引言", "方法", "结果", "结论", "参考文献"
- Spanish: "Resumen", "Introducción", "Métodos", "Resultados", "Conclusiones", "Referencias"
- Arabic: "الملخص", "المقدمة", "الطرق/المنهجية", "النتائج", "الخاتمة", "المراجع"
- French: "Résumé", "Introduction", "Méthodes", "Résultats", "Conclusion", "Références"
- German: "Zusammenfassung", "Einleitung", "Methoden", "Ergebnisse", "Fazit/Schlussfolgerung", "Literatur"
- Portuguese: "Resumo", "Introdução", "Métodos", "Resultados", "Conclusão", "Referências"
- Hindi: "सारांश", "परिचय", "विधियाँ", "परिणाम", "निष्कर्ष", "संदर्भ"
Exclusions (negative cues):
Figure/table captions (begin with tokens aligning to a nearby visual/grid; e.g., "Figure/Fig./Table", plus multilingual variants listed above).
Running headers/footers, page numbers, watermark text.
Standalone labels inside figures/diagrams.
Edge cases to still count as headings:
Two-line headings (main title + subtitle) with consistent display style.
Number-only headings followed by a separate title line.
Section markers with leading icons or ornaments.
Boundary preference:
Include the full display line(s) comprising the heading and any directly attached subtitle; exclude subsequent paragraph text and unrelated decorative elements.
"""


LISTING = """
Object: "Code listing / Pseudocode region" on a scanned document page
A contiguous block presenting source code, shell commands, logs, or algorithmic pseudocode.
Visual/structural cues (positive):
Monospaced typeface; consistent character width; strong indentation patterns (spaces/tabs).
Line-oriented layout; optional left/right gutters with line numbers.
Language tokens and symbols: braces {}, parentheses (), brackets [], semicolons ;, operators ==, !=, :=, ->; string quotes ' ", backticks `.
Comment markers (#, //, /* … */, --, %, ; in Lisp), directives (import, def, class, public, return, for, while, try, catch), or pseudocode keywords (procedure, Input:, Output:, for each).
Shaded/boxed background, thin border, or caption such as "Listing", "Code", "Algorithm"; optional language tag ("Python", "C++", "Bash").
Multilingual caption tokens (non-exhaustive):
- English: "Listing", "Code", "Algorithm"
- Russian: "Листинг", "Код", "Алгоритм"
- Chinese (简体): "代码清单", "代码", "算法"
- Spanish: "Listado", "Código", "Algoritmo"
- Arabic: "قائمة", "شفرة", "خوارزمية"
- French: "Listing", "Code", "Algorithme"
- German: "Listing", "Code", "Algorithmus"
- Portuguese: "Listagem", "Código", "Algoritmo"
- Hindi: "सूची", "코ड", "कलन विधि"
Minimal sentence punctuation and no text reflow across page columns.
Exclusions (negative cues):
Paragraph prose with inline code words but proportional font and text wrapping.
Mathematical display equations (centered formulas with fraction bars, Σ, ∫) not arranged as lines of code.
Tables that just happen to use a monospaced font.
Edge cases to still count as listings:
Wrapped long lines with continuation markers.
Terminal transcripts prefixed with prompts ($, C:\\>) mixed with output.
Pseudocode mixing math symbols (≤, ≥, ∈) but preserving line-based, indented structure.
Boundary preference:
Include the full boxed/shaded region, any line numbers, and the immediate caption/title tied to the listing; exclude surrounding paragraphs and unrelated figure captions.
"""

FORMULA = """
Object: "Mathematical formula / Display equation region" on a scanned document page
A standalone, non-inline math expression set apart from running text.
Visual/structural cues (positive):
Centered or left-aligned block with extra vertical spacing above/below; not part of a paragraph line.
Math typography and operators: fraction bars, radicals √, summation/product/integral symbols (Σ, Π, ∫), limits, arrows, comparison symbols (≤, ≥, ≈), Greek letters, subscripts/superscripts.
Multi-line alignment around relation symbols (=, ≤, ⇒) or piecewise cases with a large left brace.
Matrices/vectors with bracketed arrays; stacked constructs (binomials, limits).
Equation numbering or tags typically right-aligned: "(1)", "(2a)", "[3]", or references like "Eq. (4)".
Short textual tokens common in math: min, max, argmin, s.t., Re, Im, sin, log, exp.
Common equation/caption tokens across major languages (non-exhaustive):
- English: "Equation", "Eq.", "Formula"
- Russian: "Формула", "Уравнение"
- Chinese (简体): "公式", "方程", and numbering like "式 (1)"
- Spanish: "Ecuación", "Ecuac.", "Fórmula"
- Arabic: "معادلة", "صيغة"
- French: "Équation", "Eq.", "Formule"
- German: "Gleichung", "Formel"
- Portuguese: "Equação", "Fórmula"
- Hindi: "समीकरण", "सूत्र"
Exclusions (negative cues):
Inline math within paragraphs (embedded between words without block spacing).
Pseudocode/algorithm blocks in monospaced font, even if they contain math symbols.
Tables of numeric values or variable definitions formatted as lists.
Edge cases to still count as formulas:
Objective-and-constraints blocks (e.g., "min … s.t. …") rendered as a grouped display.
Numbered equations split across line breaks or with continuation alignment.
Rotated or slightly skewed equations; equations with adjacent short "where:" lines (treat "where" explanations as paragraph unless typographically included in the display block).
Boundary preference:
Include the full display expression and its equation tag/number; exclude preceding/following explanatory sentences and unrelated captions.
"""

COLUMN = """
Object: "Running header / footer region" on a scanned document page
A narrow strip at the top (header) or bottom (footer) margin containing repeating metadata across pages.
Visual/structural cues (positive):
Positioned within the page margin, separated from the body by extra whitespace or a thin rule.
Small font size relative to body text; often single-line or two-line.
Repeating content across pages: page number (Arabic/Roman), running title/section title, authors, journal/publisher, date, DOI/ISSN, confidentiality stamps, or logos.
Typical tokens (English): "Page", "p.", "pp.", "Vol.", "No.", "©", year; alignment to left/center/right or mirrored on facing pages.
Multilingual patterns (non-exhaustive):
- Russian: "Стр.", "С.", "Страница", "Том", "№"
- Chinese (简体): "页", "第…页", "卷", "期"
- Spanish: "Pág.", "Página", "Vol.", "N.º"/"No."
- Arabic: "صفحة", "مجلد", "العدد"
- French: "p.", "pp.", "vol.", "n°"/"no", "numéro"
- German: "S.", "Seite", "Bd.", "Nr."
- Portuguese: "p.", "pág.", "Vol.", "Nº"
- Hindi: "पृष्ठ", "खंड", "संख्या"
(Identifiers like "DOI" and "ISSN" typically appear unchanged across languages.)
Exclusions (negative cues):
Footnotes: multi-line small text anchored by superscript markers from the body; usually sits just above the footer strip.
Figure/table captions near the bottom/top of columns.
Watermarks diagonally across the page or background stamps unrelated to margins.
Edge cases to still count as header/footer:
Single-appearance on the first page (title page) if placement and style match margin metadata.
Headers/footers with decorative lines, logo blocks, or alternating even/odd page content.
Slightly cropped or skewed margin areas due to scanning.
Boundary preference:
Include only the marginal strip(s) (top and/or bottom) containing the repeating metadata; exclude nearby body text and footnotes.
"""

HEADER = """
Object: “Heading / Title region” on a scanned document page
A short line (or small block) of display text that names a document, section, or subsection.
Visual/structural cues (positive):
Font size larger than body text and/or increased weight (bold), small caps, or distinctive typeface; often centered or left-aligned with extra whitespace above/below.
Numbering patterns: “1”, “1.1”, “A.”, “I.”, “Chapter 3”, “Section 2”, “Appendix A”; Russian analogs: “Глава 3”, “Раздел 2”, “Приложение A”.
Case/typography cues: Title Case, ALL CAPS, or small caps; no end-of-line hyphenation.
Positioned at the top of a page/column or immediately preceding a paragraph; may include decorative rules above/below.
Common heading tokens across major languages (non-exhaustive):
English: “Abstract”, “Introduction”, “Methods”, “Results”, “Conclusion(s)”, “References”
Russian: “Аннотация”, “Введение”, “Методы/Методика”, “Результаты”, “Заключение”, “Литература/Ссылки”
Chinese (简体): “摘要”, “引言”, “方法”, “结果”, “结论”, “参考文献”
Spanish: “Resumen”, “Introducción”, “Métodos”, “Resultados”, “Conclusiones”, “Referencias”
Arabic: “الملخص”, “المقدمة”, “الطرق/المنهجية”, “النتائج”, “الخاتمة”, “المراجع”
French: “Résumé”, “Introduction”, “Méthodes”, “Résultats”, “Conclusion”, “Références”
German: “Zusammenfassung”, “Einleitung”, “Methoden”, “Ergebnisse”, “Fazit/Schlussfolgerung”, “Literatur”
Portuguese: “Resumo”, “Introdução”, “Métodos”, “Resultados”, “Conclusão”, “Referências”
Hindi: “सारांश”, “परिचय”, “विधियाँ”, “परिणाम”, “निष्कर्ष”, “संदर्भ”
Exclusions (negative cues):
Figure/table captions (begin with tokens like “Figure/Fig./Table”, “Рис.”, “Таблица”, “图/表”, “شكل/جدول”) aligned to a nearby visual or grid.
Running headers/footers, page numbers, footnotes, watermarks.
Standalone labels inside figures/diagrams.
Edge cases to still count as headings:
Two-line headings (main title + subtitle) with consistent display style.
Number-only headings followed by a separate title line.
Section markers with leading icons or ornaments.
Boundary preference:
Include the full display line(s) comprising the heading and any directly attached subtitle; exclude subsequent paragraph text and unrelated decorative elements.
"""
