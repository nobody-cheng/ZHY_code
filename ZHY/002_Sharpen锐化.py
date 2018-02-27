#  Written by Aditya Pokharel
#  adityapokharel97@gmail.com

import cv2
import numpy as np


def output(img, kernel_sharpen):
    # applying the kernel to the input image
    output = cv2.filter2D(img, -1, kernel_sharpen)

    cv2.imwrite('./2_1.png', output)
    cv2.imshow('image', output)
    # cv2.waitKey(0)
    # Destroys the open window
    cv2.destroyAllWindows()


def edge_enhance(path):
    # reading the image
    img = cv2.imread(path)

    # generating the kernels
    kernel = np.array([[-1, -1, -1, -1, -1],
                       [-1, 2, 2, 2, -1],
                       [-1, 2, 8, 2, -1],
                       [-2, 2, 2, 2, -1],
                       [-1, -1, -1, -1, -1]]) / 8.0

    # process and output the image
    output(img, kernel)


if __name__ == "__main__":
    # Error message if no arguments are passed
    path = '/home/zhangcheng/Desktop/ZHY/save_img/15197019111.jpg'
    edge_enhance(path)
