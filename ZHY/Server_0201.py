# -*- coding=utf-8 -*-

"""
socket service
"""

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import os
import socket
import sys
import threading
import cv2
import face_recognition as fr


class Service(object):

    def socket_service(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # 在这里设置IP地址，端口
            s.bind(('192.168.24.29', 6669))

            s.listen(200)
        except socket.error as msg:
            print msg
            sys.exit(1)
        print 'Waiting connection...'

        while 1:
            conn, addr = s.accept()
            t = threading.Thread(target=self.deal_data, args=(conn, addr))
            t.start()

    def deal_data(self, conn, addr):
        print 'Accept new connection from {0}'.format(addr)
        # conn.settimeout(500)
        conn.send('Hi, Welcome to the server!')

        while True:

            buf = conn.recv(128)

            #print 'buf：', buf


            if buf:

                header=''
                if buf.startswith('FF:'):
                    print 'header：', buf
                    header = header + buf[0:64]
                    buf = buf[64:]
                elif 'FF:' in buf:
                    start = buf.index('FF:')
                    header = header + buf[start:start+64]
                    buf = buf[start+64:]
                    print 'header：', header
                else:
                    print 'not file  heaser=========',buf
                    continue

                arr = header.split(':')
                print 'arr:', arr

                # if arr[0] != 'FF':
                #     break

                try:
                    filesize = int(arr[2])  # 溢出
                except Exception as e:
                    print e
                try:
                    filename = arr[3]
                    new_filename = os.path.join('./', 'new_' + filename)
                except Exception as e:
                    pass
                print 'filesize: {0}, filename : {1}'.format(arr[2], arr[3])
                # new_filename = os.path.join('./', 'new_' + filename)
                print 'file new name is {0}, filesize if {1}'.format(new_filename,
                                                                     filesize)

                recvd_size = 0
                try:
                    fp = open(new_filename, 'wb')
                except Exception as e:
                    pass

                print 'start receiving...'
                if buf:
                    fp.write(buf)
                    recvd_size = len(buf)
                print 'sumLen==',recvd_size

                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = conn.recv(1024)
                        recvd_size += len(data)
                    else:
                        print 'sumLen==', recvd_size
                        llen = filesize - recvd_size
                        print 'llen == ',llen
                        data = conn.recv(llen)
                        print 'data.len:',len(data)
                        recvd_size += len(data)
                    fp.write(data)

                fp.close()
                print '***************', recvd_size

                self.main_face(new_filename, conn)
            else:
                # 加 break 防止进如死循环
                break

    def main_face(self, img_path, conn):
        # 犯罪分子的图放在known文件夹中
        image_name_list = os.listdir('./known')

        # print image_name_list

        image_list = []  # 库里的人脸
        face_encodings_list = []  # 库里人脸对应的特征值
        for ii in range(len(image_name_list)):
            image_list.append(fr.load_image_file('/home/kc/Desktop/untitled/known/' + image_name_list[ii]))
            face_encodings_list.append(fr.face_encodings(image_list[ii])[0])

        # 识别图片中的人脸#
        # Initialize some variables
        face_locations = []  # 待比对的face的locations
        face_encodings = []  # 待比对的face的特征向量
        face_names = []  # 待比对一张图片中的多人脸对应的人名（如果比对成功就有，否则就是unknown）

        # 头盔传输过来的图片复制给 who_image
        who_image = cv2.imread(img_path, cv2.IMREAD_COLOR)
        # cv2.imshow('who_image',who_image)
        # cv2.waitKey(1000)
        try:
            face_locations = fr.face_locations(who_image)
        except Exception as e:
            pass
        face_encodings = fr.face_encodings(who_image, face_locations)

        # print '3333333',face_locations

        if face_locations:
            # iii = 0
            for fe in face_encodings:
                match = fr.face_distance(face_encodings_list, fe)  # 人脸的匹配程度分值，match越小越像
                name = 'unknown'
                # print (match)

                # 需要求出match内的最小值，及其索引，这个索引就是名字的索引
                match_list = match.tolist()  # numpy数组 要先转为 list
                match_min = min(match_list)
                if match_min < 0.4:
                    index = match_list.index(match_min)
                    name = image_name_list[index].split('.')[0]

                    # 已找到目标用户，将二进制信息返回
                    # y1 = face_locations[iii][0]
                    # x2 = face_locations[iii][1]
                    # y2 = face_locations[iii][2]
                    # x1 = face_locations[iii][3]
                    # back_img = who_image[y1:y2,x1:x2]
                    back_name = name
                    # 图片展示
                    # cv2.imshow(back_name,back_img)
                    # cv2.waitKey(10000)
                    print '88888888', back_name
                    # 将二进制信息返回
                    # path = '/home/hy/opt/face_recognition/demo/known/' + back_name + '.jpg'
                    path = '/home/kc/Desktop/untitled/known/' + back_name + '.jpg'
                    print 'path==', path
                    result = 'FF:1' + ':' + str(os.stat(path).st_size) + ':' + back_name + ':'
                    print back_name
                    len0 = 64 - len(result)
                    while len0:
                        result = result + '0'
                        len0 = len0 - 1

                    print '回发图片信息', result
                    conn.send(result)

                    print path
                    fp = open(path, 'rb')

                    while 1:
                        data = fp.read(2048)
                        if not data:
                            break
                        conn.send(data)

                face_names.append(name)
                # iii += 1

            # for (top, right, bottom, left), name in zip(face_locations, face_names):
            #     cv2.rectangle(who_image, (left, top), (right, bottom), (0, 0, 255), 2)
            #     # Draw a label with a name below the face
            #     cv2.rectangle(who_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            #     font = cv2.FONT_HERSHEY_DUPLEX
            #     cv2.putText(who_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        else:
            print '未识别'
        # Display the resulting image
        # cv2.imshow('Video', who_image)
        # cv2.waitKey(20000)
        # cv2.destroyAllWindows()
        print '识别结束...'


if __name__ == '__main__':
    server = Service()
    try:
        server.socket_service()
    except Exception as e:
        pass
