import base64
from PIL import Image
from io import BytesIO


def pict_save_b64(b64_image, img_path):
    image = Image.open(BytesIO(base64.b64decode(b64_image)))
    image.save(img_path, 'PNG')


def pict_read_b64(img_path):
    with open(img_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z
