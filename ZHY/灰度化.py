# RGB 转换为灰度图、二值化图
from PIL import Image
import cv2

I = Image.open('/home/zhangcheng/Desktop/ZHY/white_img/P1.jpg')
L = I.convert('L')  # 转化为灰度图
L.save('1.jpg')

im = cv2.imread('1.jpg', 0)
eq = cv2.equalizeHist(im)  # 灰度图片直方图均衡化
cv2.imwrite('vi2.jpg', eq)  # 保存图片在当前目录下
