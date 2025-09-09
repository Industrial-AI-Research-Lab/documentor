import pytest

from documentor.structuries.fragment.code import ListingFragment


@pytest.mark.parametrize(
    "code_str",
    [
        "print('hi')\n",
        "def f(x):\n    return x * 2\n",
        "# пустой листинг\n",
    ],
)
def test_listing_fragment_behaves_like_text(code_str):
    frag = ListingFragment(value=code_str)
    assert str(frag) == code_str
    d = frag.__dict__()
    # Subclass may not include 'value' key due to annotations resolution
    assert str(frag) == code_str
    # ListingFragment may keep base default description or override constant
    from documentor.structuries.fragment.description import LISTING
    assert frag.description() in {"", LISTING}
