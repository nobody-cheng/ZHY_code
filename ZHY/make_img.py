# -*- coding=utf-8 -*-
import cv2
from os.path import join
from os import listdir, path
from skimage import util
import os
import numpy as np
import random
import time


def is_image_file(filename):
    return any(filename.endswith(extension) for extension in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'])


def getImgName(dataset_dir):
    read_person_name = [join(dataset_dir, x) for x in listdir(dataset_dir) if is_image_file(x)]
    return read_person_name


# 定义旋转rotate函数
def rotate(image, angle, center=None, scale=1.0):
    # 获取图像尺寸
    (h, w) = image.shape[:2]
    # 若未指定旋转中心，则将图像中心设为旋转中心
    if center is None:
        center = (w / 2, h / 2)
    # 执行旋转
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    # 返回旋转后的图像
    return rotated


def skimage2opencv(src):
    src *= 255
    src = np.uint8(src)  # cv2.error: C:\projects\opencv-python\opencv\modules\imgproc\src\color.cpp:11073:
    #  error: (-215) depth == 0 || depth == 2 || depth == 5 in function cv::cvtColor
    cv2.cvtColor(src, cv2.COLOR_RGB2BGR)
    return src


def opencv2skimage(src):
    cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    src.astype(float)
    src /= 255
    return src


def makeImg(img):
    # x1 = cv2.blur(img, (3, 3))  # 模板大小3*3
    x2 = cv2.blur(img, (5, 5))  # 模板大小3*3
    # x3 = rotate(img, 10)
    # x4 = rotate(img, -10)
    # x5 = rotate(img, 20, scale=0.9)
    # x6 = rotate(img, -20, scale=0.9)
    # sk_img = opencv2skimage(img)
    sk_img = img
    x7 = util.random_noise(sk_img, mode="gaussian")
    # x8 = util.random_noise(sk_img, mode="salt")
    x9 = util.random_noise(sk_img, mode="poisson")
    x7 = skimage2opencv(x7)
    # x8 = skimage2opencv(x8)
    x9 = skimage2opencv(x9)
    h, w, _ = img.shape
    x10 = cv2.resize(img, (int(w * 0.4), int(h * 0.4)), cv2.INTER_AREA)
    x10 = cv2.resize(x10, (w, h), cv2.INTER_LINEAR)

    tmp_img_list = [x2,x7,x9, x10]
    return tmp_img_list


def create_img(img_path_list, save_base_path):
    tmp_img_list = []
    img_name_list = []
    file_num = 0
    save_base_path_1 = save_base_path
    for img_path in img_path_list:
        file_num = file_num + 1
        img = cv2.imread(img_path)
        h, w, _ = img.shape
        img = cv2.resize(img, (int(w * 0.5), int(h * 0.5)))
        tmp_img_list = makeImg(img)  # 读取一张图片就先造了一部分的图片[x1,x2,...,xn]
        img_name_jpg = img_path.split("/")[-1]
        if "_" not in img_name_jpg:
            continue
        img_name = img_name_jpg.split("_")[0]  # get img name likes "0000117" ,is a person
        print(img_name)
        if 0 == file_num % 1000 :
            # save_base_path = join(save_base_path, str(file_num))
            save_base_path_1 = save_base_path + "/" + str(file_num)
        save_path = join(save_base_path_1, img_name)
        if path.exists(save_path) is False:
            os.makedirs(save_path)  # 新建保存造好数据的文件夹

        # 在造好的一部分图中，再将每一种扩充以下几种
        # 比如一张图造了9张图，然后这9张图中每一张都再造别的三种图，一共造了3*9 = 27 种类图
        len_list = len(tmp_img_list)
        new_num = 0  # 记录保存图片的名字次序
        for i in range(len_list):
            new_img_tmp = tmp_img_list[i]
            tmp_path = join(save_path, img_name) + "_" + str(random.randint(10000, 20000)) + ".png"
            cv2.imwrite(tmp_path, new_img_tmp)

            # 保存灰度图
            gray = cv2.cvtColor(new_img_tmp, cv2.COLOR_BGR2GRAY)
            tmp_path = join(save_path, img_name) + "_" + str(random.randint(10000, 20000)) + ".png"
            cv2.imwrite(tmp_path, gray)  # 保存红色通道

            # 调整明亮度
            bright_img = np.uint16(new_img_tmp) * 1.2
            bright_img = np.where(bright_img < 255, bright_img, 255)
            tmp_path = join(save_path, img_name) + "_" + str(random.randint(10000, 20000)) + ".png"
            cv2.imwrite(tmp_path, bright_img)  # 保存红色通道
            # black_img = np.where(new_img_tmp > 20 , new_img_tmp,20)
            black_img = new_img_tmp * 0.7
            tmp_path = join(save_path, img_name) + "_" + str(random.randint(10000, 20000)) + ".png"
            cv2.imwrite(tmp_path, black_img)


if __name__ == "__main__":
    start = time.time()
    # 修改“/”
    file_path = "/home/kcadmin/zip_out"
    save_base_path = "/opt/makeface"
    # file_path = "D:\\makeFece"
    # save_base_path = "D:\\makeFece_out"
    # img_path_list = getImgName(file_path)
    img_path_list = []
    for (root, dirs, files) in os.walk(file_path):  # 列出windows目录下的所有文件和文件名
        for filename in files:
            img_path = os.path.join(root, filename)
            img_path_list.append(img_path)

    create_img(img_path_list, save_base_path)
    print('all time: ', time.time() - start)

