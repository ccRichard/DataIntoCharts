#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2016-12-12 15:46:11
# Author     : cc
# Description: stack_bar

import os
from collections import OrderedDict

from echarts import Echart, Legend, Bar, Axis, Toolbox, Grid
from func.common import count_list

# 数据配置
title = '场景加载时间'
subtext = '对比不同机型不同场景的平均加载时间'
login_kw = 'TIME:Enter_LOGIN'
load_kw = 'TIME:SCENE'
sence_kw = {"1":"登录场景login", "2":"创角场景rolecreate",
             "3":"主城ceshichangjing_001", "4":"主城2main2",
             "5":"俱乐部jiazhuangditu_001", "6":"新主城xiaoditu_001",
             "TIME:Enter_LOGIN":"登录Enter_LOGIN"}

# 从log中获取数据
def data_clean(file):
    file_data = OrderedDict()

    f = open(file)
    for line in f.readlines():
        if line.find(login_kw) != -1:
            key = login_kw
            value = float(line.split(':')[-1].replace(' ',''))
        elif line.find(load_kw) != -1:
            temp = line.split(load_kw)[-1].split('LOAD:')
            key = temp[0].replace(' ','')
            value = float(temp[1].replace(' ',''))
        if not key:
            continue
        if key not in file_data:
            file_data[key] = list()
        file_data[key].append(value)
    f.close()

    # 通过log文件名获取设备名称
    phone_name = os.path.split(file)[1].replace('.log', '')
    phone_data = OrderedDict()

    for key in file_data:
        if key in sence_kw:
            newkey = sence_kw[key]
        else:
            newkey = key
        phone_data[newkey] = round(count_list(file_data[key])['median'],2)

    return phone_name, phone_data


# 将多个log文件里的数据有序化
def arrage_logs(files):
    manchines = list()
    log_datas = list()
    sences = list()
    datas = OrderedDict()

    for file in files:
        log_name, log_data = data_clean(file)
        manchines.append(log_name)
        log_datas.append(log_data)
        log_sences = log_data.keys()
        for sence in log_sences:
            if sence not in sences:
                sences.append(sence)

    for sence in sences:
        xlist = list()
        for data in log_datas:
            if sence not in data:
                xlist.append(0)
            else:
                xlist.append(data[sence])
        datas[sence] = xlist

    return manchines, datas


def client_x9_load_scenes_draw_bar(filelist):
    pname, datas = arrage_logs(filelist)
    tags = list()
    json_data = list()

    # 绘图对象，包含标题设置
    chart = Echart(title, subtext)
    # 绘图数据
    for data in datas:
        tags.append(data)
        chart.use(Bar(data, datas[data], stack='time', label={'normal':{'show':True}}))
    # x轴
    chart.use(Axis('category', 'bottom', '设备', pname, axisLabel={'rotate':40,'interval':0}, axisTick={'interval':0}))
    # y轴
    chart.use(Axis('value', 'left', '秒'))
    # 标签，与之相似的还有个叫visualmap，但未实现
    chart.use(Legend(tags, top=80))
    # 添加工具栏，默认在右上角
    chart.use(Toolbox())
    # 设置绘图区域的位置，默认上留120，下留100
    chart.use(Grid())
    chart.json
    json_data.append(chart.get_opt())

    return json_data

if __name__ == '__main__':
    pass

