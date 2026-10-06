"""Prep a photo for ASCII conversion: remove bg -> CLAHE contrast -> composite on white.
Usage: python scripts/prep_photo.py source-photo.jpg   (writes source-prepped.png)"""
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
img = Image.open(src).convert("RGB")
cut = remove(img)                              # RGBA, background transparent
rgba = np.array(cut)
alpha = rgba[..., 3].astype(np.float32) / 255.0

gray = cv2.cvtColor(rgba[..., :3], cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
gray = clahe.apply(gray).astype(np.float32)

out = gray * alpha + 255.0 * (1.0 - alpha)     # background -> pure white
Image.fromarray(out.astype(np.uint8), "L").save("source-prepped.png")
print("wrote source-prepped.png")
