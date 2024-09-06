import os
from utils import InstaImage, AspectRatio, get_save_filename
from PIL import Image, ImageOps
import numpy as np
import argparse

ASPECT_RATIOS = {
    "square": AspectRatio(width=1080, height=1080),
    "landscape": AspectRatio(width=1080, height=566),
    "portrait": AspectRatio(width=1080, height=1350)
    }
QUALITY = {
    1: Image.Resampling.BILINEAR,
    2: Image.Resampling.BICUBIC,
    3: Image.Resampling.LANCZOS
    }

parser = argparse.ArgumentParser(
    description="Simple CLI tool which adds borders to images for Instagram.")

parser.add_argument("source", metavar="SOURCE",
                    help="source directory containing files or single file \
                    \nspecify relative or absolute paths")
parser.add_argument("dest", metavar="DEST",
                    help="destination directory \nspecify relative or absolute paths")
parser.add_argument("-p", "--percentage", default=0.8, type=float,
                    help="image length as percentage of canvas edge with tightest fit")
parser.add_argument("-ct", "--canvas-type", default="square", choices=["square", "landscape", "portrait"],
                    help="canvas (background) type supported by Instagram")
parser.add_argument("-cc", "--canvas-color", default="#ffffff",
                    help="hex code of canvas (background) color, example: '#ff0000' for red \
                    '#' can be included or omitted")
parser.add_argument("-rq", "--resize-quality", default=2, choices=range(1,4),
                    help="quality for resampling when fitting source image onto canvas \
                    \n1 = lowest quality, fastest performance \
                    \n2 = higher quality, slower performance \
                    \n3 = highest quality, slowest performance")

if __name__ == "__main__":
    args = parser.parse_args()

    # check valid source/destination
    if not (os.path.isdir(args.source) or os.path.isfile(args.source)):
        msg = f"Specified source directory/file path is invalid. {args.source}"
        raise ValueError(msg)
    if not (os.path.isdir(args.dest)):
        msg = f"Specified destination directory path is invalid. {args.dest}"
        raise ValueError(msg)
    
    # check valid canvas color
    if args.canvas_color.lower().startswith("#") and (len(args.canvas_color) != 7):
        msg = f"Specified canvas (background) color is invalid: {args.canvas_color}"
        raise ValueError(msg)
    elif args.canvas_color.startswith([str(i) for i in range(10)]) and (len(args.canvas_color) != 6):
        msg = f"Specified canvas (background) color is invalid: {args.canvas_color}"
        raise ValueError(msg)
    
    # TODO: check percentage?

    if os.path.isabs(args.source):
        src = args.source
    else:
        src = os.path.abspath(args.source)
    
    if os.path.isabs(args.dest):
        dst = args.dest
    else:
        dst = os.path.abspath(args.dest)
    
    percentage = args.percentage
    canvas_type = ASPECT_RATIOS[args.canvas_type]
    canvas_color = args.canvas_color
    resample = QUALITY[args.resize_quality]

    if os.path.isfile(src):  # single file
        # filename = os.path.split(src)[-1]  # get file name + extension
        # filename, ext = os.path.splitext(filename)  # split file name and extension
        # filename = f"{filename}_{args.canvas_type}" + ext
        filename = get_save_filename(src, args.canvas_type)
        savedir = os.path.join(dst, filename)
        img = InstaImage(src, canvas_type, percentage, resample, canvas_color)
        img.process()
        img.save(savedir)
    # elif os.path.isdir(src):
    


# INPUTS
# photo_path = os.getcwd() + "/test_images/image_1.jpg"  # input image path
# save_path = os.getcwd() + "/test_images/image_1_insta.jpg"  # output image dir
# percent = 0.8  # percentage of longest img edge wrt same orientation canvas edge
# canvas_type = PORTRAIT
# # canvas_color = (255, 255, 255)  # can also be hex string
# canvas_color = "#ff0000"
# # quality 1: downscale = hamming, upscale = bilinear
# # quality 2: downscale/upscale = bicubic
# # quality 3: downscale/upscale = lanczos
# resample = Image.Resampling.LANCZOS

# # FLOW
# canvas_ratio = canvas_type.width / canvas_type.height

# # open image
# img_ = Image.open(photo_path)
# img = ImageOps.exif_transpose(img_)
# img_.close()

# # get image ratio
# img_ratio = img.size[0] / img.size[1]

# # compute width & height and resize
# if (img_ratio) >= canvas_ratio:
#     # image aspect ratio wider than canvas aspect ratio
#     width = int(np.round(canvas_type.width * percent))
#     height = int(np.round(width / img_ratio))
# else:
#     # image aspect ratio narrower than canvas aspect ratio
#     height = int(np.round(canvas_type.height * percent))
#     width = int(np.round(height * img_ratio))

# img = img.resize((width, height), resample)

# # create canvas and paste image
# bg = Image.new(img.mode, (canvas_type.width, canvas_type.height), canvas_color)
# bg.paste(img, ((canvas_type.width - width) // 2, (canvas_type.height - height) // 2))

# bg.save(save_path)