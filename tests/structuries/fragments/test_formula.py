import pytest
from PIL import Image

from documentor.data.structures.fragment.formula import ImageFormulaFragment, LatexFormulaFragment
from documentor.data.structures.fragment.description import FORMULA


@pytest.mark.parametrize("fname", ["single_formula.png"])
def test_image_formula_fragment_description(fname, data_dir):
    img = Image.open(data_dir / "fragments" / fname)
    frag = ImageFormulaFragment(value=img)
    # Description is provided via classmethod
    assert frag.description() == FORMULA
    s = str(frag)
    assert isinstance(s, str) and len(s) > 10


def test_latex_formula_fragment_text_and_description():
    latex = r"\\frac{a}{b} + \\sqrt{x}"
    frag = LatexFormulaFragment(value=latex)
    assert str(frag) == latex
    # Latex formula description via classmethod
    assert frag.description() == FORMULA
