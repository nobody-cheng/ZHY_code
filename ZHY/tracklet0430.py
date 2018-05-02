# -*- coding: utf-8 -*-
import time
import math
import numpy as np
from scipy.optimize import linear_sum_assignment
import KalmanFilter_trace


class Tracklet(object):
    def __init__(self):
        self.tracklet = {}
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
        # return 返回遮挡和走出去人的id,此ID为确定的 cost_coor，feature_cost 大于阈值离开当前帧
        realid_list = []
        tempid_list = []
        for rid in self.all_data.keys():
            realid_list.append(rid)
        for tid in self.all_trace_cost.keys():
            tempid_list.append(tid)

        for i in range(len(row_ind)):
            cost = Matrix_cost[row_ind[i], col_ind[i]]
            # 匹配 更新id
            if cost < 0.7:
                self.all_trace_cost[realid_list[i]] = self.all_trace_cost.pop(self.all_trace_cost[tempid_list[i]])
            # 不匹配
            else:
                # 1. 遮挡

                # 2. 离开

                # 3. 新进入
                pass
        return

    def GetInPersonTempId(self, cost):
        # return 返回走进的人的id,此ID为临时的
        return 2
        # 1. 新进入，进行比对前面的特征，如无，新增
        # 2. 有插入新的一个信息

    def GetTempIdToId(self, cost):
        # tempid,id
        return 2

    def UpdataCurrentState(self, data):
        # 1. {id: [time, feature, coordinate], id: [time, feature, coordinate]}
        # 1. tracklet = {'people': [[[1, 11, xy], [2,22,xy], [3,33,xy]], [[1, 11, xy], [2,22,xy], [3,33,xy]], ]} 时间 id 坐标 特征

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
            index.append([tim, face_feature, coordinate])
            self.all_data[key] = index

    def Updatatracklet(self, outid, intempid, tempIdToID):
        for id in outid:
            if (len(self.tracklet[id]) == 15)
                self.tracklet[id].
                del ()
            self.tracklet[id].append([0, 0])
        for tempid in intempid:
            # DO:新得到一个self.tracklet没有的ID
            self.tracklet[newid].append([curtime, self.cur_state[tempid].coordinate, self.cur_state[tempid].fearture])
        for key, value in tempIdToID.iterms:
            if (len(self.tracklet[id]) == 15)
                self.tracklet[id].
                del ()
            self.tracklet[key].append(
                [curtime, self.cur_state[value].coordinate, self.cur_state[value].fearture])
        return 2

    def run(self, data):
        # 1.数据格式预处理，保存到curr_state,格式和kalman_state一样
        self.UpdataCurrentState(self, data)
        # kalman距离矩阵 w1权重 距离cost
        for tempid in self.all_data.keys():
            trace = KalmanFilter_trace.SingleKalmanFilter()
            x = self.all_data[tempid][2][0]
            y = self.all_data[tempid][2][1]
            result = trace.Trace(x, y, trace.currentMesure, trace.currentPredict)
            # 位置距离cost
            self.all_trace_cost[tempid].append(w1 * self.posistion_dis(result.currentMesure, result.lastPredict))
            # result.currentPredict
        # feature 矩阵 w2权重 特征的cost
        # ?????
        # Matrix_cost = all_trace_cost + feature cost
        Matrix_cost = [[]]  # 矩阵匹配 需要传入距离和特征cost的值，得到行，列
        row_ind, col_ind = linear_sum_assignment(Matrix_cost)
        # 检验cost，如果大于0-1之间的某个阈值就认为匹配无效,认为是新加入、遮挡、出界
        self.GetOutPersonID(Matrix_cost, row_ind, col_ind)

        # # 2.curr_state和kalman_state计算cost
        # cost = self.CalCost(kalman_state, curr_state, self.w1, self.w2)
        #
        # outId = self.GetOutPersonID(cost)
        #
        # intempId = self.GetOutPersonID(cost)
        #
        # tmpIdToId = self.GetTempIdToId(cost)
        #
        # # 更新5s的字典
        # self.Updatatracklet(self, outId, intempId, tmpIdToId)
        # # 预测下一个状态
        # self.kalman(data)
