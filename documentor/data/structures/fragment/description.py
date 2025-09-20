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



CAPTION = """
Object: "Caption region" on a scanned document page
A short descriptive text accompanying visual elements such as figures, tables, or formulas.
Visual/structural cues (positive):
Positioned directly above or below the associated visual element; often separated by minimal whitespace.
Smaller font size than body text; may be italicized, centered, or left-aligned.
Common caption tokens and their variants: "Figure", "Fig.", "Table", "Tab.", "Equation", "Eq.", "Formula".
Multilingual caption tokens (non-exhaustive):
- Russian: "Рис.", "Рисунок", "Таблица", "Табл.", "Формула", "Уравнение"
- Chinese (简体): "图", "图表", "表", "表格", "公式", "方程"
- Spanish: "Figura", "Fig.", "Tabla", "Ecuación", "Fórmula"
- Arabic: "شكل", "صورة", "جدول", "معادلة", "صيغة"
- French: "Figure", "Fig.", "Tableau", "Équation", "Formule"
- German: "Abb.", "Abbildung", "Tabelle", "Gleichung", "Formel"
- Portuguese: "Figura", "Tabela", "Equação", "Fórmula"
- Hindi: "आकृति", "चित्र", "तालिका", "समीकरण", "सूत्र"
Often includes numbering or labeling: "Figure 1:", "Table 2:", "Equation (3)".
May contain brief explanatory text describing the visual content.
Exclusions (negative cues):
Standalone text blocks not clearly associated with visual elements.
Running headers/footers or page numbers.
Figure/table content itself (the actual visual data).
Edge cases to still count as captions:
Multi-line captions with continuation text.
Captions with special formatting or symbols.
Captions that appear slightly separated from their visual elements due to layout constraints.
Boundary preference:
Include the complete caption text and any associated numbering; exclude the visual element itself and unrelated surrounding text.
"""

FOOTNOTE = """
Object: "Footnote region" on a scanned document page
Supplementary information or citations appearing at the bottom of pages, referenced by markers in the main text.
Visual/structural cues (positive):
Positioned in the lower portion of the page, often separated from body text by a horizontal rule or extra whitespace.
Smaller font size than body text; typically single-spaced or slightly condensed.
Referenced by superscript markers in the main text: ¹, ², ³, *, †, ‡, or bracketed numbers [1], [2], [3].
Common footnote patterns:
- Citation references: "Author, Title, Journal, Year"
- Explanatory notes: "See also...", "Note that...", "For details see..."
- Cross-references: "See Section 2.1", "As mentioned above"
- Legal disclaimers or copyright information
Multilingual footnote markers (non-exhaustive):
- Russian: "¹", "²", "³", "[1]", "[2]", "См. также", "Примечание"
- Chinese (简体): "¹", "²", "注", "参见", "详见"
- Spanish: "¹", "²", "Nota", "Véase", "Ver también"
- Arabic: "¹", "²", "ملاحظة", "انظر أيضاً"
- French: "¹", "²", "Note", "Voir aussi", "Cf."
- German: "¹", "²", "Anmerkung", "Siehe auch", "Vgl."
- Portuguese: "¹", "²", "Nota", "Ver também", "Cf."
- Hindi: "¹", "²", "नोट", "देखें भी", "संदर्भ"
Exclusions (negative cues):
Page footers containing only page numbers or publication information.
Figure/table captions that happen to appear at the bottom of the page.
Running headers or watermarks.
Edge cases to still count as footnotes:
Footnotes that continue across multiple lines.
Footnotes with complex formatting or multiple references.
Footnotes that appear slightly above the page footer due to space constraints.
Boundary preference:
Include the complete footnote text and its reference marker; exclude the horizontal rule separator and unrelated footer content.
"""

LIST_ITEM = """
Object: "List item region" on a scanned document page
Individual elements within ordered, unordered, or definition lists.
Visual/structural cues (positive):
Consistent indentation from the left margin; uniform spacing between items.
Leading markers: bullets (•, ◦, ▪, ▫), numbers (1., 2., 3.), letters (a., b., c.), or dashes (-, —).
Monospaced or proportional font; may be indented with spaces or tabs.
Common list patterns:
- Unordered lists: bullet points, dashes, or other symbols
- Ordered lists: Arabic numerals, Roman numerals, or letters
- Definition lists: term followed by definition, often with special formatting
- Nested lists: sub-items with increased indentation
Multilingual list markers (non-exhaustive):
- Russian: "•", "◦", "1.", "2.", "а)", "б)", "—", "–"
- Chinese (简体): "•", "1.", "2.", "（一）", "（二）", "—", "—"
- Spanish: "•", "◦", "1.", "2.", "a)", "b)", "—", "–"
- Arabic: "•", "◦", "1.", "2.", "أ)", "ب)", "—", "–"
- French: "•", "◦", "1.", "2.", "a)", "b)", "—", "–"
- German: "•", "◦", "1.", "2.", "a)", "b)", "—", "–"
- Portuguese: "•", "◦", "1.", "2.", "a)", "b)", "—", "–"
- Hindi: "•", "◦", "1.", "2.", "क)", "ख)", "—", "–"
Exclusions (negative cues):
Paragraph text that happens to start with a number or symbol.
Table rows or cells that appear list-like but are part of a grid structure.
Code blocks or algorithm steps that use indentation but aren't true lists.
Edge cases to still count as list items:
Multi-line list items that wrap to subsequent lines.
List items with complex formatting or nested structures.
List items that use non-standard markers or formatting.
Boundary preference:
Include the complete list item text and its marker; exclude surrounding paragraph text and unrelated content.
"""

PAGE_HEADER = """
Object: "Page header region" on a scanned document page
Repeating header information appearing at the top of pages, typically containing section titles, chapter names, or other metadata.
Visual/structural cues (positive):
Positioned within the top margin, separated from body text by extra whitespace or a thin horizontal rule.
Smaller font size than body text; often single-line or two-line maximum.
Repeating content across multiple pages: section titles, chapter names, document titles, or author names.
Common header patterns:
- Section titles: "Chapter 3: Methods", "Section 2.1: Introduction"
- Document titles: "Research Paper Title", "Annual Report 2024"
- Author information: "J. Smith, M. Johnson", "Department of Computer Science"
- Publication metadata: "Journal Name", "Volume 15, Issue 3"
Multilingual header patterns (non-exhaustive):
- Russian: "Глава 3: Методы", "Раздел 2.1", "Исследование", "Автор: И. Иванов"
- Chinese (简体): "第3章：方法", "2.1节", "研究报告", "作者：张三"
- Spanish: "Capítulo 3: Métodos", "Sección 2.1", "Investigación", "Autor: J. García"
- Arabic: "الفصل 3: الطرق", "القسم 2.1", "البحث", "المؤلف: أ. أحمد"
- French: "Chapitre 3: Méthodes", "Section 2.1", "Recherche", "Auteur: P. Martin"
- German: "Kapitel 3: Methoden", "Abschnitt 2.1", "Forschung", "Autor: H. Müller"
- Portuguese: "Capítulo 3: Métodos", "Seção 2.1", "Pesquisa", "Autor: M. Silva"
- Hindi: "अध्याय 3: विधियाँ", "खंड 2.1", "अनुसंधान", "लेखक: आ. शर्मा"
Exclusions (negative cues):
Main document titles or section headings that appear only once.
Figure/table captions that happen to appear at the top of the page.
Page numbers that appear alone without other header content.
Edge cases to still count as page headers:
Headers with decorative elements or logos.
Headers that alternate between even and odd pages.
Headers that appear slightly below the page top due to layout constraints.
Boundary preference:
Include the complete header text and any associated formatting; exclude the horizontal rule separator and unrelated content.
"""

PAGE_FOOTER = """
Object: "Page footer region" on a scanned document page
Repeating footer information appearing at the bottom of pages, typically containing page numbers, publication information, or other metadata.
Visual/structural cues (positive):
Positioned within the bottom margin, separated from body text by extra whitespace or a thin horizontal rule.
Smaller font size than body text; often single-line or two-line maximum.
Repeating content across multiple pages: page numbers, publication information, copyright notices, or document metadata.
Common footer patterns:
- Page numbers: "Page 15", "15", "p. 15", "pp. 15-16"
- Publication info: "Journal of Research, Vol. 15, No. 3", "© 2024 Author"
- Document metadata: "Confidential", "Draft", "Version 2.1"
- Legal information: "All rights reserved", "Proprietary and confidential"
Multilingual footer patterns (non-exhaustive):
- Russian: "Стр. 15", "Страница 15", "Журнал исследований, Том 15", "© 2024 Автор"
- Chinese (简体): "第15页", "页15", "研究期刊，第15卷", "© 2024 作者"
- Spanish: "Pág. 15", "Página 15", "Revista de Investigación, Vol. 15", "© 2024 Autor"
- Arabic: "صفحة 15", "ص 15", "مجلة البحث، المجلد 15", "© 2024 المؤلف"
- French: "p. 15", "Page 15", "Revue de Recherche, Vol. 15", "© 2024 Auteur"
- German: "S. 15", "Seite 15", "Forschungszeitschrift, Bd. 15", "© 2024 Autor"
- Portuguese: "p. 15", "Página 15", "Revista de Pesquisa, Vol. 15", "© 2024 Autor"
- Hindi: "पृष्ठ 15", "पृ. 15", "अनुसंधान पत्रिका, खंड 15", "© 2024 लेखक"
Exclusions (negative cues):
Footnotes that appear at the bottom of the page.
Figure/table captions that happen to appear at the bottom of the page.
Watermarks or background text that appears across the page.
Edge cases to still count as page footers:
Footers with decorative elements or logos.
Footers that alternate between even and odd pages.
Footers that appear slightly above the page bottom due to layout constraints.
Boundary preference:
Include the complete footer text and any associated formatting; exclude the horizontal rule separator and unrelated content.
"""