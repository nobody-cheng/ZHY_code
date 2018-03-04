#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: send.py
socket client
"""

import socket
import os
import sys
import struct
reload(sys)
sys.setdefaultencoding('utf-8')

class sock_cli(object):
    def socket_client(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 绑定IP和端口
            s.connect(('10.4.91.103', 6666))
        except socket.error as msg:
            print msg
            sys.exit(1)

        print s.recv(1024)

        while 1:
            filepath = raw_input('please input file path: ')
            if os.path.isfile(filepath):

                fileinfo_size = struct.calcsize('128sl')
                filename = 'FF:01:'+str(os.stat(filepath).st_size)+':'+os.path.basename(filepath)+':'
                # fhead = struct.pack('128sl', filename,
                #                     os.stat(filepath).st_size)

                len0 = 64-len(filename)
                while len0:
                    filename = filename+'0'
                    len0 = len0-1

                s.send(filename)

                print 'filename：',filename
                # print 'client filepath: {0}'.format(filepath)

                fp = open(filepath, 'rb')
                while 1:
                    data = fp.read(2048)
                    if not data:
                        # print '{0} file send over...'.format(filepath)
                        break
                    s.send(data)

                # if s.recv(1024):
                #     print '识别成功后返回二进制的数据：',s.recv(1024)
                # else:
                #     print s.recv(1024)
                continue

if __name__ == '__main__':
    cli = sock_cli()
    cli.socket_client()

    """
    /home/hy/opt/face_recognition/demo/zhou.jpg
    /home/hy/opt/face_recognition/demo/测试.jpg
    /home/hy/opt/face_recognition/demo/who.jpg
    /home/hy/opt/face_recognition/demo/5555.jpg
    
    """