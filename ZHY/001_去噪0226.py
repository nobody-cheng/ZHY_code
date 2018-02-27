import cv2
"""
图像的去噪时间太长
"""

imgName = '/home/zhangcheng/Desktop/ZHY/white_img/P1.jpg'

# 去除噪点
img = cv2.imread(imgName)
cv2.imshow('img', img)
rows, cols, channels = img.shape
print(rows, cols)
dst = img.copy()

a = 1.1
b = 30

for i in range(rows):
    for j in range(cols):
        for c in range(3):
            color = img[i, j][c] * a + b
            if color > 255:
                dst[i, j][c] = 255
            elif color < 0:
                dst[i, j][c] = 0

cv2.imshow('dst', dst)
cv2.waitKey(0)

cv2.destroyAllWindows()
