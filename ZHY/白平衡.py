from PIL import Image, ImageOps
#
# ImageOps.equalize(Image.open("/home/zhangcheng/Desktop/python/img/P2.jpg")).save("e.jpg")

# ImageOps.autocontrast(Image.open("/home/zhangcheng/Desktop/python/img/P1.jpg")).save("e_1.jpg")


import cv2
import numpy as np


img = cv2.imread('/home/zhangcheng/Desktop/ZHY/save_img/P3_1.jpg')


def gimp(img, perc=0.05):
    for channel in range(img.shape[2]):
        mi, ma = (np.percentile(img[:, :, channel], perc), np.percentile(img[:, :, channel], 100.0 - perc))
        img[:, :, channel] = np.uint8(np.clip((img[:, :, channel] - mi) * 255.0 / (ma - mi), 0, 255))
    return img


def gray_world(nimg):
    nimg = nimg.transpose(2, 0, 1).astype(np.uint32)
    mu_g = np.average(nimg[1])
    nimg[0] = np.minimum(nimg[0] * (mu_g / np.average(nimg[0])), 255)
    nimg[2] = np.minimum(nimg[2] * (mu_g / np.average(nimg[2])), 255)
    return nimg.transpose(1, 2, 0).astype(np.uint8)

out = img
out = gray_world(out)
out = gimp(out, 0.05)
cv2.imwrite('wb5.bmp', out)
