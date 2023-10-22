# coding=utf-8
import cv2
import numpy as np
import pytesseract
from PIL import Image


def captcha_OCR(image_bytes):
    arr = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)  # 'Load it as it is'
    # cv2.imshow("image", img)
    # cv2.waitKey()
    # 轉灰
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 2值化
    ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # 轉成 PIL
    im_pil = Image.fromarray(img)
    im_np = np.asarray(im_pil)
    code = pytesseract.image_to_string(im_np)
    code = code.strip().replace(" ", "")
    return code
