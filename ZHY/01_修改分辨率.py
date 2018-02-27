import os
import time
from PIL import Image


def alter(path, object):
    s = os.listdir(path)

    count = 1
    for i in s:
        document = os.path.join(path, i)

        img = Image.open(document)
        out = img.resize((3028, 2042))
        # listStr = [str(int(time.time())), str(count)]
        # fileName = ''.join(listStr)
        fileName = os.path.splitext(i)[0]
        out.save(object + os.sep + '{}_1.jpg'.format(fileName))
        count = count + 1


img_path = '/home/zhangcheng/Desktop/ZHY/img'
out_path = '/home/zhangcheng/Desktop/ZHY/save_img'

alter(img_path, out_path)
