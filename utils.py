import os
from collections import namedtuple
import numpy as np
from PIL import Image, ImageOps

def get_save_filename(path_: str, *additions) -> str:
    filename = os.path.split(path_)[-1]  # get file name + extension
    filename, ext = os.path.splitext(filename)  # split file name and extension
    filename = f"{filename}_{"_".join(additions)}" + ext
    return filename

AspectRatio = namedtuple("AspectRatio", ["width", "height"])


class InstaImage:

    def __init__(
            self,
            file_path: str,
            canvas_type: AspectRatio,
            percent: float,
            resample: Image.Resampling,
            canvas_color: str
            ) -> None:
        img_ = Image.open(file_path)
        self.img = ImageOps.exif_transpose(img_)
        img_.close()
        self.canvas_type = canvas_type
        self.canvas_color = canvas_color
        self.percent = percent
        self.resample = resample
    
    def process(self) -> None:
        self.bg = Image.new(
            self.img.mode,
            (self.canvas_type.width, self.canvas_type.height),
            self.canvas_color
            )
        
        self.bg.paste(
            self.img,
            ((self.canvas_type.width - self.width) // 2, (self.canvas_type.height - self.height) // 2)
            )
        
    def save(self, save_dir):
        self.bg.save(save_dir)

    def _fit_to_canvas(self) -> None:
        img_ratio = self.img.size[0] / self.img.size[1]
        canvas_ratio = self.canvas_type.width / self.canvas_type.height

        # image aspect ratio wider than canvas aspect ratio
        if (img_ratio) >= canvas_ratio:
            width = int(np.round(self.canvas_type.width * self.percent))
            height = int(np.round(width / img_ratio))
        
        # image aspect ratio narrower than canvas aspect ratio
        else:
            height = int(np.round(self.canvas_type.height * self.percent))
            width = int(np.round(height * img_ratio))
        
        img = img.resize((width, height), self.resample)