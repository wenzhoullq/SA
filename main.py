# -*- coding: utf-8 -*-
from __future__ import print_function
import math
import random
import bisect
from simanneal import Annealer
#  执行脚本
# 1.pip install simanneal  # from pypi
#
# 2.pip install -e git+https://github.com/perrygeo/simanneal.git#egg=requests
def distance(a, b):
    """Calculates distance between two latitude-longitude coordinates."""
    R = 3963  # radius of Earth (miles)
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    return math.acos(math.sin(lat1) * math.sin(lat2) +
                     math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)) * R


class TravellingSalesmanProblem(Annealer):
    """Test annealer with a travelling salesman problem.
    """

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, citys, noHubCity, hubCity, p, dis, thoughout):
        self.dis = dis
        self.thoughout = thoughout
        self.noHubCity = noHubCity
        self.hubCity = hubCity
        self.p = p
        self.citys = citys
        super(TravellingSalesmanProblem, self).__init__(citys)  # important!

    def move(self):
        """Swaps two cities in the route."""
        # no efficiency gain, just proof of concept
        # demonstrates returning the delta energy (optional)
        initial_energy = self.energy()
        i = random.randint(0, len(self.citys) - 1)
        while i not in noHubCitySet: i = random.randint(0, len(self.citys) - 1)
        self.citys[i] = choose(hubCity, p, i)
        # print(self.energy() )
        return self.energy() - initial_energy

    def energy(self):
        """计算碳排放和成本"""
        # 单位公里每吨成本(元)
        cost = 0.5

        # a 枢纽机场之间运输的成本折扣系数
        a = 0.8

        # 巡航阶段单位公里的碳排放(吨)
        t1 = 1.5

        # 爬坡/降落阶段单位公里的碳排放(吨)
        t2 = 200

        # 单位吨碳的价格
        p = 90
        # 能量
        e = 0
        # 计算非枢纽节点到非枢纽节点的排放和成本
        city = self.citys
        dis = self.dis
        thoughout = self.thoughout
        no = self.noHubCity
        hub = self.hubCity
        for i in no:
            for j in no:
                if i == j: continue
                ## 经济成本 = 距离 * 流量 * 单价
                target1, target2 = city[i], city[j]
                e += (dis[i][target1] + dis[j][target2]) * thoughout[i][j] * cost
                ## 碳排放 = (爬坡 + 距离 * 流量 * 单位距离的碳排放) * 单位吨碳的价格
                e += (t2 * 2 + (dis[i][target1] + dis[j][target2]) * thoughout[i][j] * t1) * p
                # 如果连接的不是同一个枢纽机场,则需要计算转运的成本和碳排放
                if target1 != target2:
                    # 经济成本
                    e += dis[target1][target2] * thoughout[i][j] * cost
                    # 碳排成本
                    e += (t2 + dis[target1][target2] * thoughout[i][j] * t1) * p
        # 计算非枢纽节点到枢纽节点的排放和成本
        for i in no:
            for j in hub:
                target = city[i]
                # 计算经济成本
                e += dis[i][target] * thoughout[i][j] * cost
                # 碳排成本
                e += (t2 + dis[i][target] * thoughout[i][j] * t1) * p
                # 如果枢纽城市不是目标城市
                if target != j:
                    #经济成本
                    e += dis[target][j] * thoughout[i][j] * cost
                    #碳排成本
                    e += (t2 + dis[target][j] * thoughout[i][j] * t1) * p
        # 计算枢纽节点到非枢纽节点的排放和成本
        for i in hub:
            for j in no:
                target = city[j]
                # 计算经济成本
                e += dis[i][target] * thoughout[i][j] * cost
                # 碳排成本
                e += (t2 + dis[i][target] * thoughout[i][j] * t1) * p
                # 如果枢纽城市不是目标城市
                if target != i:
                    #经济成本
                    e += dis[target][i] * thoughout[i][j] * cost
                    #碳排成本
                    e += (t2 + dis[target][i] * thoughout[i][j] * t1) * p
        # 计算枢纽节点到枢纽节点的排放和成本
        for i in hub:
            for j in hub:
                if i == j: continue
                ## 经济成本 = 距离 * 流量 * 单价
                e += dis[i][j]  * thoughout[i][j] * cost
                ## 碳排放 = (爬坡 + 距离 * 流量 * 单位距离的碳排放) * 单位吨碳的价格
                e += (t2  + dis[i][j]  * thoughout[i][j] * t1) * p
        return e


def shuffle(city, noHubCitySet, hubCity):
    for i in range(len(city)):
        if i in noHubCitySet:
            j = random.randint(0, len(city) - 1)
            while j not in hubCity: j = random.randint(0, len(city) - 1)
            city[i] = j
    return city


def choose(hubCity, p, i):
    sum = [0] * (len(hubCity) + 1)
    j = 1
    for k in range(0, 15):
        if p[i][k] > 0:
            sum[j] = sum[j - 1] + p[i][k]
            j += 1
    num = random.random()
    index = bisect.bisect_left(sum, num)
    return index - 1
def cal(city,dis,thoughout,no,hub):
    """计算碳排放和成本"""
    # 单位公里每吨成本(元)
    cost = 0.5

    # a 枢纽机场之间运输的成本折扣系数
    a = 0.8

    # 巡航阶段单位公里的碳排放(吨)
    t1 = 1.5

    # 爬坡/降落阶段单位公里的碳排放(吨)
    t2 = 200

    # 单位吨碳的价格
    p = 90
    # 能量
    e = 0
    # 计算非枢纽节点到非枢纽节点的排放和成本
    for i in no:
        for j in no:
            if i == j: continue
            ## 经济成本 = 距离 * 流量 * 单价
            target1, target2 = city[i], city[j]
            e += (dis[i][target1] + dis[j][target2]) * thoughout[i][j] * cost
            ## 碳排放 = (爬坡 + 距离 * 流量 * 单位距离的碳排放) * 单位吨碳的价格
            e += (t2 * 2 + (dis[i][target1] + dis[j][target2]) * thoughout[i][j] * t1) * p
            # 如果连接的不是同一个枢纽机场,则需要计算转运的成本和碳排放
            if target1 != target2:
                # 经济成本
                e += dis[target1][target2] * thoughout[i][j] * cost
                # 碳排成本
                e += (t2 + dis[target1][target2] * thoughout[i][j] * t1) * p
    # 计算非枢纽节点到枢纽节点的排放和成本
    for i in no:
        for j in hub:
            target = city[i]
            # 计算经济成本
            e += dis[i][target] * thoughout[i][j] * cost
            # 碳排成本
            e += (t2 + dis[i][target] * thoughout[i][j] * t1) * p
            # 如果枢纽城市不是目标城市
            if target != j:
                #经济成本
                e += dis[target][j] * thoughout[i][j] * cost
                #碳排成本
                e += (t2 + dis[target][j] * thoughout[i][j] * t1) * p
    # 计算枢纽节点到非枢纽节点的排放和成本
    for i in hub:
        for j in no:
            target = city[j]
            # 计算经济成本
            e += dis[i][target] * thoughout[i][j] * cost
            # 碳排成本
            e += (t2 + dis[i][target] * thoughout[i][j] * t1) * p
            # 如果枢纽城市不是目标城市
            if target != i:
                #经济成本
                e += dis[target][i] * thoughout[i][j] * cost
                #碳排成本
                e += (t2 + dis[target][i] * thoughout[i][j] * t1) * p
    # 计算枢纽节点到枢纽节点的排放和成本
    for i in hub:
        for j in hub:
            if i == j: continue
            ## 经济成本 = 距离 * 流量 * 单价
            e += dis[i][j]  * thoughout[i][j] * cost
            ## 碳排放 = (爬坡 + 距离 * 流量 * 单位距离的碳排放) * 单位吨碳的价格
            e += (t2  + dis[i][j]  * thoughout[i][j] * t1) * p
    return e

if __name__ == '__main__':

    # latitude and longitude for the twenty largest U.S. cities
    dis = [
        [0, 1466, 1679, 1967, 2493, 1200, 2266, 981, 1178, 730, 1133, 2842, 1774, 1034, 690],
        [1466, 0, 940, 620, 1100, 805, 1166, 799, 964, 2191, 658, 3261, 873, 955, 828],
        [1697, 940, 0, 1390, 1757, 1699, 711, 1618, 1782, 2346, 1047, 2258, 1911, 647, 1039],
        [1967, 620, 1390, 0, 548, 1099, 1357, 1255, 1308, 2672, 873, 3836, 567, 1528, 1389],
        [2493, 1100, 1757, 548, 0, 1606, 1046, 1990, 1762, 3142, 1379, 4400, 1100, 1860, 1873],
        [1200, 805, 1699, 1099, 1606, 0, 2089, 240, 176, 1849, 656, 3653, 717, 1215, 841],
        [2266, 1116, 711, 1357, 1046, 2089, 0, 1870, 2042, 2935, 1364, 2920, 1680, 1228, 1570],
        [981, 799, 1618, 1255, 1990, 240, 1870, 0, 273, 1630, 503, 3412, 929, 1104, 630],
        [1178, 964, 1782, 1308, 1762, 176, 2042, 273, 0, 1364, 761, 3649, 878, 1351, 887],
        [730, 2191, 2346, 2672, 3142, 1849, 2935, 1630, 1364, 0, 1859, 3230, 2242, 1683, 1339],
        [1133, 658, 1047, 873, 1379, 656, 1364, 503, 761, 1859, 0, 3061, 910, 735, 530],
        [2842, 3261, 2258, 3836, 4400, 3653, 2920, 3412, 3649, 3230, 3061, 0, 4238, 2306, 2747],
        [1774, 873, 1911, 567, 1100, 717, 1680, 929, 878, 2242, 910, 4238, 0, 1932, 1312],
        [1034, 955, 647, 1528, 1860, 1215, 1228, 1104, 1351, 1683, 735, 2306, 1932, 0, 474],
        [690, 828, 1039, 1389, 1873, 841, 1570, 630, 887, 1339, 530, 2747, 1312, 474, 0],
    ]
    thoughout = [
        [0, 56.8, 160.8, 213.2, 73, 108, 110.8, 91.6, 386.9, 96.4, 56.1, 71.2, 60.8, 104.8, 41.2],
        [47.5, 0, 44.5, 27.7, 30, 18.7, 47.2, 30.5, 40.2, 5, 0, 9.9, 13.2, 8.9, 4.8],
        [111.2, 34.2, 0, 94.2, 12.2, 26.4, 82, 26.1, 88.3, 22.8, 26.2, 26.4, 7.1, 38.6, 18],
        [151.5, 20.9, 72.2, 0, 119.5, 106.9, 68.5, 51, 170.6, 9.3, 46.6, 18.3, 41.1, 49.1, 27.3],
        [60.6, 25.8, 17.4, 100.5, 0, 21.8, 26.9, 23.6, 71.5, 5.5, 22.6, 4.3, 18, 21, 21.7],
        [74.5, 14.8, 16.5, 78.2, 15.8, 0, 11.1, 3.4, 0, 12.2, 18.2, 4.2, 38.8, 18.5, 15.7],
        [78.7, 34.7, 65.3, 51.8, 19.3, 5, 0, 9.7, 53.2, 7.5, 9.8, 5.1, 13.4, 30, 27.3],
        [68.9, 19.9, 18, 45.1, 13.4, 3, 5.2, 0, 0, 5.2, 8.9, 5.6, 19.7, 11.8, 18.1],
        [284.5, 27.1, 64.5, 128.2, 56.9, 0, 42.6, 1, 0, 57.3, 66.9, 30.2, 90.8, 62.8, 36.4],
        [71.5, 4, 15, 7.6, 4.2, 10.8, 5, 4, 2, 0, 7.4, 4, 12.6, 7, 11.3],
        [44.4, 0, 22.3, 13.2, 17.2, 15, 8.4, 8, 3, 4, 0, 7.4, 4, 12.6, 7, 11.3],
        [46.1, 7.7, 22.6, 13.2, 3.2, 3, 4, 4, 4, 3, 4, 0, 3, 31.7, 11.7],
        [43.8, 11.3, 6, 35.4, 15.5, 34.7, 10.2, 17.6, 5, 8.2, 10.2, 2, 0, 6.1, 8.6],
        [68.7, 7, 31.6, 35.6, 16.4, 12.7, 21.8, 9, 6, 5, 11.8, 22.7, 4, 0, 6.2],
        [28.8, 3.5, 13.5, 21.8, 12, 12.2, 19.5, 10, 7, 9.6, 4, 9.2, 7, 2, 0],
    ]

    # initial state, a randomly-ordered itinerary
    hubCity = [0, 1, 2, 3, 8]
    hubCitySet = set(hubCity)
    noHubCity = [4, 5, 6, 7, 9, 10, 11, 12, 13, 14]
    noHubCitySet = set(noHubCity)
    n = len(dis)
    city = [0] * n
    for i in range(len(dis)):
        city[i] = i
    z = [[0] * n for _ in range(n)]
    sumz = [0] * n
    p = [[0] * n for _ in range(n)]
    sumd = 0
    sumt = 0
    for i in range(0, n):  ## i是枢纽节点
        for j in range(0, n):  ## j是非枢纽节点
            if i in hubCitySet and j in noHubCitySet:
                sumd += dis[j][i] + dis[i][j]
                sumt += thoughout[j][i] + thoughout[i][j]
    for i in range(0, n):  ## i是枢纽节点
        for j in range(0, n):  ## j是非枢纽节点
            if i in hubCitySet and j in noHubCitySet:
                zz = ((thoughout[j][i] + thoughout[i][j]) / sumt) / ((dis[j][i] + dis[i][j]) / sumd)
                z[j][i] = zz
            sumz[j] = sumz[j] + z[j][i]

    for i in range(n):  ## i是枢纽城市 是被连接的
        if i not in hubCitySet: continue
        for j in range(n):  ## j是非枢纽城市 是起点
            if j not in noHubCitySet: continue
            p[j][i] = z[j][i] / sumz[j]
    ## 生成随机的初始结果
    citys = shuffle(city, noHubCitySet, hubCity)
    print(citys)
    print("energy-start:",cal(citys, dis, thoughout, noHubCity, hubCity))
    tsp = TravellingSalesmanProblem(citys, noHubCity, hubCity, p, dis, thoughout)
    tsp.Tmax = 2200000000
    tsp.Tmin = 1800000000
    tsp.steps = 100000
    # tsp.set_schedule(tsp.auto(minutes=0.2))
    # # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()
    print(citys)
    for i in range(len(citys)):
        if i== citys[i]:print(i,"是枢纽机场")
        else:print(i,"是非枢纽机场,它所连接的枢纽机场是",citys[i])
    print("energy-end:",cal(citys,dis, thoughout, noHubCity, hubCity))
