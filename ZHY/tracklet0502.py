# -*- coding: utf-8 -*-
import time
import math
import numpy as np
from scipy.optimize import linear_sum_assignment
import KalmanFilter_trace


class Tracklet(object):
    def __init__(self):
        self.tracklet = {'people': []}
        self.all_data = {}
        self.all_trace_cost = {}
        self.threshold = 0.8
        self.w1 = 0
        self.w2 = 0

    def posistion_dis(self, peo, peo2):
        # 计算两个人之间的位置坐标距离
        midp1 = self.cal_mid_point(peo)
        midp2 = self.cal_mid_point(peo2)
        tmp = (midp1[0] - midp2[0]) ** 2 + (midp1[1] - midp2[1]) ** 2
        dis = math.sqrt(tmp)
        dis = 1 / (1 + math.exp(-dis))  # 归一化
        return dis

    def feature_dis(self, peo, peo2):
        # 计算特征相似度,采用余弦距离
        fea1 = np.array(peo)
        fea2 = np.array(peo2)
        fdist = np.dot(fea1, fea2) / (np.linalg.norm(fea1, 2) * np.linalg.norm(fea2, 2))
        return fdist

    def cal_mid_point(self, rec):
        midpos = [0, 0]
        # 计算矩形块中心点位置
        midpos[0] = (rec[0] + rec[2]) / 2
        midpos[1] = (rec[1] + rec[3]) / 2
        return midpos

    def CalCost(self, kalman_state, curr_state, w1, w2):
        # 计算 kalman 和 cur 坐标损失
        cost_coor = w1 * self.posistion_dis(kalman_state, curr_state)
        # 计算 kalman和cur 的特征损失
        feature_cost = w2 * self.feature_dis(kalman_state, curr_state)
        return cost_coor, feature_cost

    def GetOutPersonID(self, Matrix_cost, row_ind, col_ind):
        # return 返回遮挡和走出去人的id,此ID为确定的 cost_coor, feature_cost 大于阈值离开当前帧
        realid_list = []
        tempid_list = []
        feature_list = []

        for tid in self.all_trace_cost.keys():
            tempid_list.append(tid)

        for info_list in self.tracklet['people']:
            for info in info_list:
                for ii in info:
                    feature_list.append(ii[3])
                    realid_list.append(ii[0])

        for i in range(len(row_ind)):
            cost = Matrix_cost[row_ind[i], col_ind[i]]
            # 匹配 更新id
            if cost < 0.7:
                self.all_trace_cost[realid_list[i]] = self.all_trace_cost.pop(self.all_trace_cost[tempid_list[i]])
            # 不匹配
            else:
                # 1. 遮挡 离开 丢失
                for info_list in self.tracklet['people']:
                    feature_cur = info_list[i][3]
                    if feature_cur in feature_list:
                        print('Target Miss')
                        return info_list[i][0]  # 返回id
                    else:
                        # 2. 新进入
                        print('New Target')
                        # 插入 [id 时间 坐标 特征]
                        tracklet_list = self.tracklet['people']
                        self.tracklet['people'] = tracklet_list.append(info_list[i])
        return

    def UpdataCurrentState(self, data):
        # 1.tracklet = {'people': [[[1, 11, xy, fe], [2, 22, xy, fe], [3, 33, xy, fe]],
        # [[1, 11, xy, fe], [2,22,xy, fe], [3,33,xy, fe]]]} id 时间 坐标 特征
        data = dict(data)
        id_list = []
        face_feature = []
        coordinate = []
        tim = []
        for key in data.keys():
            index = []
            tim.append(key.split('_')[0])
            id_list.append(key)
            face_feature.append(data[key][2])  # 填入输入数据中feature的序号
            coordinate.append(data[key][5])
            index.append([key, tim, face_feature, coordinate])
            tracklet_list = self.tracklet['people']
            self.tracklet['people'] = tracklet_list.append(index)
            if len(self.tracklet['people']) > 15:  # 1秒3帧 删除前面
                del self.tracklet['people'][0:len(self.tracklet) - 1]

    # def Updatatracklet(self, outid, intempid, tempIdToID):
    #     for id in outid:
    #         if (len(self.tracklet[id]) == 15)
    #             self.tracklet[id].
    #             del ()
    #         self.tracklet[id].append([0, 0])
    #     for tempid in intempid:
    #         # DO:新得到一个self.tracklet没有的ID
    #         self.tracklet[newid].append([curtime, self.cur_state[tempid].coordinate, self.cur_state[tempid].fearture])
    #     for key, value in tempIdToID.iterms:
    #         if (len(self.tracklet[id]) == 15)
    #             self.tracklet[id].
    #             del ()
    #         self.tracklet[key].append(
    #             [curtime, self.cur_state[value].coordinate, self.cur_state[value].fearture])
    #     return 2

    def run(self, data):
        # 1.数据格式预处理，保存到curr_state,格式和 kalman_state 一样
        self.UpdataCurrentState(self, data)
        # kalman距离矩阵 w1权重 距离 cost
        # tracklet = {'people': [[[1, 11, xy], [2,22,xy], [3,33,xy]], [[1, 11, xy], [2,22,xy], [3,33,xy]]]} id 时间 坐标 特征
        for temp_list in self.tracklet['people']:
            trace = KalmanFilter_trace.SingleKalmanFilter()
            for tem in temp_list:
                x = tem[2][0]
                y = tem[2][1]
                result = trace.Trace(x, y, trace.currentMesure, trace.currentPredict)
                # 位置距离cost
                self.all_trace_cost[tem[0]].append(w1 * self.posistion_dis(result.currentMesure, result.lastPredict))
                # result.currentPredict
        # feature 矩阵 w2权重 特征的cost
        # ?????
        # Matrix_cost = all_trace_cost + feature cost
        Matrix_cost = [[]]  # 矩阵匹配 需要传入距离和特征cost的值，得到行，列
        row_ind, col_ind = linear_sum_assignment(Matrix_cost)
        # 检验cost，如果大于0-1之间的某个阈值就认为匹配无效,认为是新加入、遮挡、出界
        self.GetOutPersonID(Matrix_cost, row_ind, col_ind)
        # tmpIdToId = self.GetTempIdToId(cost)
        # # 更新5s的字典
        # self.Updatatracklet(self, outId, intempId, tmpIdToId)
        # # 预测下一个状态
        # self.kalman(data)
