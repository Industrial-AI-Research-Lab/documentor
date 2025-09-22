import base64
from io import BytesIO

import pytest
from PIL import Image

from documentor.data.structures.fragment.image import ImageFragment
from documentor.data.structures.fragment.description import IMAGE


@pytest.mark.parametrize(
    "fname",
    [
        "single_image.png",
    ],
)
def test_image_fragment_roundtrip_base64(fname, data_dir):
    img_path = data_dir / "fragments" / fname
    image = Image.open(img_path)

    frag = ImageFragment(value=image, format="PNG", encoding="utf-8")

    b64 = str(frag)
    assert isinstance(b64, str) and len(b64) > 10

    # Re-create fragment from base64
    frag2 = ImageFragment.from_base64(b64, format="PNG", encoding="utf-8")

    # Compare sizes to ensure correctness
    assert frag2.value.size == image.size
    assert frag.description() == IMAGE

    d = frag.__dict__()
    assert set(d.keys()) == {
        "value",
        "format",
        "encoding",
        "page",
        "description",
        "is_processed",
        "id",
        "bbox",
        "style",
    }
    assert d["id"] is None
    assert d["bbox"] is None
    assert d["style"] is None
    # Ensure value is valid base64
    base64.b64decode(d["value"].encode("utf-8"))
