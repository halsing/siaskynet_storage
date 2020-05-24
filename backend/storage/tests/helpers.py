import tempfile

from io import BytesIO
from PIL import Image

from django.core.files.base import File


def temp_image():
    """
    Returns a new temporary image file
    """

    image = Image.new("RGB", (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file, "jpeg")
    tmp_file.seek(0)
    return tmp_file.read()


def temp_text_file():
    """
    Returns a new temporary text file
    """
    manuscript = tempfile.NamedTemporaryFile(suffix=".txt")
    manuscript.write(b"This is my stupid paper")
    manuscript.seek(0)
    return manuscript
