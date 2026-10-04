import os.path
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile


def is_supported_image_format(filename):
    return os.path.splitext(filename)[1].lower() in [".jpg", ".jpeg", ".png", ".webp"]

def generate_thumbnail(attachment):
    if not attachment.file or not is_supported_image_format(attachment.file.name):
        return None
    try:
        attachment.file.open("rb")
        image = Image.open(attachment.file)
        image.load()
    except:
        return None

    width = 200
    format = (image.format or "JPEG").upper()
    if image.width > width:
        ratio = width / float(image.width)
        image = image.resize((width, max(1, int(image.height * ratio))))

    if format == "JPEG" and image.mode not in ["RGB", "L"]:
        image = image.convert("RGB")

    buffer = BytesIO()
    try:
        image.save(buffer, format=format)
    except:
        return None

    base = os.path.splitext(os.path.basename(attachment.file.name))[0]
    thumbfile_name = f"{base}_thumb.{format.lower()}"
    attachment.thumbnail.save(thumbfile_name, ContentFile(buffer.getvalue()), save=True)
    return attachment.thumbnail.name