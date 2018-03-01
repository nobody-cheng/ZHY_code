
import numpy as np
import cv2

img = cv2.imread('/home/zhangcheng/Desktop/ZHY/IMAGE/P1_2.jpg')
res = np.uint8(np.clip((1.5 * img + 10), 0, 255))
# tmp = np.hstack((img, res))  # 两张图片横向合并（便于对比显示）
cv2.imwrite('ld1.jpg', res)

