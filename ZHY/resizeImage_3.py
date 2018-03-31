import cv2
import os
import dlib
import numpy as np
import re

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

save_path = '/home/python/Desktop/python/image/out_img/'
video_path = '/home/python/Desktop/python/image/video/'
video_img = '/home/python/Desktop/python/image/video_img/'
face_img = '/home/python/Desktop/python/image/face_img/'
# suffix = ['jpg', 'png']

if not os.path.exists(save_path):
    os.makedirs(save_path)


def read_video(video_path):
    print('read video')
    for root, dirs, video_files in os.walk(video_path):
        p = 1
        for video in video_files:
            # read video
            videoPath = video_path + video
            print('videoPath==', videoPath)
            vc = cv2.VideoCapture(videoPath)
            c = 1

            if vc.isOpened():
                rval, frame = vc.read()
            else:
                rval = False

            timeFps = 5

            while rval:
                rval, frame = vc.read()
                if c % timeFps == 0:
                    cv2.imwrite(video_img + '{}'.format(c) + '.png', frame)
                c = c + 1
            print('Save Picture {}'.format(p))
            p += 1
            vc.release()


def read_face_img(video_img):
    for root, dirs, files in os.walk(video_img):
        count = 0
        files.sort(key=lambda index: int(re.match(r'(\d+)', index).group()))

        for file_name in files:
            print('~~~~~~~~~~~~~~~~~~~handle video_img {}~~~~~~~~~~~~~~~~~~~'.format(file_name))
            video_img_path = video_img + file_name
            image = cv2.imread(video_img_path)
            try:
                dets = detector(image, 1)
            except:
                break
            print('dets==', dets)
            for k, d in enumerate(dets):
                height = d.bottom() - d.top()
                width = d.right() - d.left()
                img_blank = np.zeros((height, width, 3), np.uint8)
                for i in range(height):
                    for j in range(width):
                        try:
                            img_blank[i][j] = image[d.top() + i][d.left() + j]
                        except:
                            continue
                cv2.imwrite(face_img + '{}'.format(count) + ".png", img_blank)
                count += 1


def resizeImage(dir):
    print('++++++++++++++++++++  resizeImage  +++++++++++++++++')
    for root, dirs, files in os.walk(dir):
        index_128, index_192, index_256, index_320 = 0, 0, 0, 0
        for file in files:
            filepath = os.path.join(root, file)
            file = filepath
            image = cv2.imread(file)  # opencv
            (h, w) = image.shape[:2]  # get img size
            print(h, w)
            if h < 112:
                continue

            elif (h >= 112) and (h <= 175):
                save_img(128, image, index_128)
                index_128 += 1

            elif (h >= 176) and (h <= 239):
                save_img(192, image, index_192)
                index_192 += 1

            elif (h >= 240) and (h <= 303):
                save_img(256, image, index_256)
                index_256 += 1

            elif h >= 304:
                save_img(320, image, index_320)
                index_320 += 1


def save_img(size, image, i):
    name = save_path + '{}'.format(size) + '_' + '{}'.format(i) + '.png'
    img_size = (size, size)
    resized = cv2.resize(image, img_size, interpolation=cv2.INTER_AREA)
    cv2.imwrite(name, resized)


if __name__ == '__main__':
    read_video(video_path)
    read_face_img(video_img)
    resizeImage(face_img)
    print('***************end********************')
