import os
from PIL import Image, ImageOps
import cv2
import numpy as np


def gimp(img, perc=0.05):
    """白平衡处理"""
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


def enhance(path, fileName):
    """锐化图片"""
    # reading the image
    img = cv2.imread(path)

    # generating the kernels
    kernel = np.array([[-1, -1, -1, -1, -1],
                       [-1, 2, 2, 2, -1],
                       [-1, 2, 8, 2, -1],
                       [-2, 2, 2, 2, -1],
                       [-1, -1, -1, -1, -1]]) / 8.0

    # process and output the image
    output(img, kernel, fileName)


def output(img, kernel_sharpen, fileName):
    # applying the kernel to the input image
    output = cv2.filter2D(img, -1, kernel_sharpen)

    cv2.imwrite('/home/zhangcheng/Desktop/ZHY/IMAGE/{}_2.jpg'.format(fileName), output)


def alter(img_path, object):
    """1.获取图片"""
    s = os.listdir(img_path)
    count = 1
    for i in s:
        document = os.path.join(img_path, i)
        print(document)
        # img = Image.open(document)
        # out = img.resize((6056, 4084))
        fileName = os.path.splitext(i)[0]
        # 调节亮度
        img = cv2.imread(document)
        res = np.uint8(np.clip((1.5 * img + 10), 0, 255))
        path = object + os.sep + '{}_1.jpg'.format(fileName)
        cv2.imwrite(path, res)
        # 裁剪后的保存路径
        # out.save(path)
        count = count + 1

        # 2.白平衡处理
        w_path = "/home/zhangcheng/Desktop/ZHY/white_img/{}.jpg".format(fileName)
        img = cv2.imread(path)
        out = img
        out = gray_world(out)
        out = gimp(out, 0.05)
        cv2.imwrite(w_path, out)

        # 高斯滤波
        kernel_size = (5, 5)
        # sigma标准差 为0时自动求标准差
        sigma = 0
        img = cv2.imread(w_path)
        img = cv2.GaussianBlur(img, kernel_size, sigma)
        cv2.imwrite(w_path, img)

        # 4.处理保存锐化后图片
        enhance(w_path, fileName)


img_path = '/home/zhangcheng/Desktop/ZHY/data'
out_path = '/home/zhangcheng/Desktop/ZHY/save_img'

alter(img_path, out_path)
