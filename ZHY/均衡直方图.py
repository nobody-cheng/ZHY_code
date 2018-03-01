# import numpy as np
# import cv2
#
# im = cv2.imread('/home/zhangcheng/Desktop/ZHY/IMAGE/P3_2.jpg', 0)   
# # cv2.imshow('image1', im)
# # cv2.waitKey(0)
#
# eq = cv2.equalizeHist(im)         #灰度图片直方图均衡化
# # cv2.imshow('image2',eq)
# # cv2.waitKey(0)
#
# cv2.imwrite('vi4.jpg', eq)      #保存图片在当前目录下

# 彩图直方图均衡化
import numpy as np
import cv2


def hisEqulColor(img):
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
    return img


im = cv2.imread('/home/zhangcheng/Desktop/ZHY/white_img/P1.jpg')
eq = hisEqulColor(im)
cv2.imwrite('lena2.jpg', eq)
