from PIL import Image
import base64
from io import BytesIO

from dataclasses import dataclass

from documentor.structuries.fragment import FragmentInterface
from documentor.structuries.fragment.description import IMAGE


@dataclass
class ImageFragment(FragmentInterface):
    """
    Implementation for image fragments that have an image value.
    """
    value: Image
    format: str = "PNG"
    encoding: str = "utf-8"
    description: str = IMAGE

    def __str__(self) -> str:
        """
        Base64 representation of the image fragment value.

        Returns:
            str: Base64 encoded string of the image.
        """
        buffered = BytesIO()
        self.value.save(buffered, format=self.format)
        return base64.b64encode(buffered.getvalue()).decode(self.encoding)

    def __dict__(self) -> dict[str, str]:
        """
        Get parameters of the image fragment.

        Returns:
            dict[str, str]: Parameters of the image fragment.
        """
        return {
            "value": str(self),
            "format": self.format,
            "encoding": self.encoding
        }

    @staticmethod
    def from_base64(b64_string: str, format: str = "PNG", encoding: str = "utf-8") -> 'ImageFragment':
        """
        Create an ImageFragment from a base64 encoded string.

        Args:
            b64_string (str): Base64 encoded string of the image.
            format (str, optional): Format of the image. Defaults to "PNG".
            encoding (str, optional): Encoding of the base64 string. Defaults to "utf-8".

        Returns:
            ImageFragment: An instance of ImageFragment.
        """
        image_data = base64.b64decode(b64_string.encode(encoding))
        image = Image.open(BytesIO(image_data))
        return ImageFragment(value=image, format=format, encoding=encoding)


