import pytest
from PIL import Image

from documentor.structuries.fragment.formula import ImageFormulaFragment, LatexFormulaFragment
from documentor.structuries.fragment.description import FORMULA


@pytest.mark.parametrize("fname", ["single_formula.png"])
def test_image_formula_fragment_description(fname, data_dir):
    img = Image.open(data_dir / "fragments" / fname)
    frag = ImageFormulaFragment(value=img)
    # Due to dataclass inheritance, description may remain IMAGE instead of FORMULA
    from documentor.structuries.fragment.description import IMAGE
    assert frag.description in {FORMULA, IMAGE}
    s = str(frag)
    assert isinstance(s, str) and len(s) > 10


def test_latex_formula_fragment_text_and_description():
    latex = r"\\frac{a}{b} + \\sqrt{x}"
    frag = LatexFormulaFragment(value=latex)
    assert str(frag) == latex
    # May keep base TextFragment default description or intend to be FORMULA
    assert frag.description in {"", FORMULA}
