import os
from PIL import Image, ImageOps
import cv2
import numpy as np


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
    # cv2.imshow('image', output)
    # cv2.waitKey(0)
    # Destroys the open window
    # cv2.destroyAllWindows()


def alter(img_path, object):
    """1.获取图片进行裁剪"""
    s = os.listdir(img_path)
    count = 1
    for i in s:
        document = os.path.join(img_path, i)
        img = Image.open(document)
        out = img.resize((3028, 2042))
        # listStr = [str(int(time.time())), str(count)]
        # fileName = ''.join(listStr)
        fileName = os.path.splitext(i)[0]
        # 裁剪后的保存路径
        path = object + os.sep + '{}_1.jpg'.format(fileName)
        out.save(path)
        count = count + 1

        # 2.白平衡处理
        w_path = "/home/zhangcheng/Desktop/ZHY/white_img/{}.jpg".format(fileName)
        img = ImageOps.autocontrast(Image.open(path))
        img.save(w_path)

        # 4.处理去噪保存锐化后图片

        enhance(w_path, fileName)


img_path = '/home/zhangcheng/Desktop/ZHY/data'
out_path = '/home/zhangcheng/Desktop/ZHY/save_img'

alter(img_path, out_path)
