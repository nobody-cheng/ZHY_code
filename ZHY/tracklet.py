# -*- coding: utf-8 -*-
import time
import math
import numpy as np


class Tracklet(object):
    def __init__(self):
        self.tracklet = []
        self.tracklet_single = []

    # 1.构造字典列表
    def put_tracklet(self, data):
        # 根据传入数据进行修改
        for key, value in data.items():
            id = value['id']
            coordinate = value['coordinate']  # (x, y)
            feature = value['feature']
            time = value['time']
            self.tracklet_single = [time, id, coordinate, feature]
            self.tracklet.append(self.tracklet_single)
            if len(self.tracklet) > 15:  # 1秒3帧，5秒3帧
                del self.tracklet[0:len(self.tracklet) - 3]
        tracklet = np.array(self.tracklet)
        return tracklet  # 返回array

    # 2.计算cost的矩阵
    def posistion_dis(self, before):
        # 计算两个人之间的位置坐标距离
        pass
    # 3.得到匹配结果

    # 4. 找出异常人，遍历tracklet进行皮队


    def get_cost(self):
        # 计算cost值
        pass

    def cal_mid_point(self, rec):
        # print(rec)
        midpos = [0, 0]
        # 计算矩形块中心点位置
        midpos[0] = (rec[0] + rec[2]) / 2
        midpos[1] = (rec[1] + rec[3]) / 2
        return midpos

    def sigmoid(self, x):
        # 将数据映射到0-1之内
        return 1 / (1 + math.exp(-x))
