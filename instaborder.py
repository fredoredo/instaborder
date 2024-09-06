import os
from collections import namedtuple
from PIL import Image, ImageOps
import numpy as np

AspectRatio = namedtuple("AspectRatio", ["width", "height"])

SQUARE = AspectRatio(width=1080, height=1080)
LANDSCAPE = AspectRatio(width=1080, height=566)
PORTRAIT = AspectRatio(width=1080, height=1350)

photo_path = os.getcwd() + "/test_images/image_1.jpg"  # input image path
save_path = os.getcwd() + "/test_images/image_1_insta.jpg"  # output image dir
percent = 1  # percentage of longest img edge wrt same orientation canvas edge
canvas_type = PORTRAIT
canvas_color = (255, 255, 255)  # can also be hex string
# quality 1: downscale = hamming, upscale = bilinear
# quality 2: downscale/upscale = bicubic
# quality 3: downscale/upscale = lanczos
resample = Image.Resampling.LANCZOS

canvas_ratio = canvas_type.width / canvas_type.height

img_ = Image.open(photo_path)
img = ImageOps.exif_transpose(img_)
img_.close()

img_ratio = img.size[0] / img.size[1]

if (img_ratio) >= canvas_ratio:
    # image aspect ratio wider than canvas aspect ratio
    width = int(np.round(canvas_type.width * percent))
    height = int(np.round(width / img_ratio))
else:
    # image aspect ratio narrower than canvas aspect ratio
    height = int(np.round(canvas_type.height * percent))
    width = int(np.round(height * img_ratio))

img = img.resize((width, height), resample)
bg = Image.new(img.mode, (canvas_type.width, canvas_type.height), canvas_color)
bg.paste(img, ((canvas_type.width - width) // 2, (canvas_type.height - height) // 2))

bg.save(save_path)