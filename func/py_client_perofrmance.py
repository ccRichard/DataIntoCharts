# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2017-4-11 11:08:23
# Author     : cc
# Description:


import sys
from collections import OrderedDict

from func.common import *

sys.path.append('../')
from echarts import Echart, Legend, Line, Axis, Tooltip, Toolbox, Grid


# 从txt文件中获取数据
def data_clean(file):
    file_data = list()

    f = open(file)
    for line in f.readlines():
        temp_list = line.split('|')
        while len(file_data) < len(temp_list):
            file_data.append(list())
        for index, value in enumerate(temp_list):
            # 第一列时间只取时分秒，其余列都按浮点数处理
            if index == 0:
                value = value.split()[-1]
            else:
                value = round(float(value), 2)
            file_data[index].append(value)
    f.close()

    return file_data


# 绘制框架图
def draw(datas, **kwargs):

    title = '缺少标题'
    if 'title' in kwargs:
        title = kwargs['title']
    subtext = ''
    if 'subtext' in kwargs:
        subtext = kwargs['subtext']
    # 绘图对象，包含标题设置
    chart = Echart(title, subtext)

    # 绘图数据
    tags = list()
    for data in datas:
        tags.append(data)
        chart.use(Line(data, datas[data]))

    x_name = ''
    y_name = ''
    x_line = list()
    if 'label' in kwargs:
        x_name = kwargs['label'][0]
        y_name = kwargs['label'][1]
        x_line = kwargs['label'][2]
    # x轴
    chart.use(Axis('category', 'bottom', x_name, data=x_line))
    # y轴
    chart.use(Axis('value', 'left', y_name))
    # 标签
    t_top = 60
    if 'top' in kwargs:
        t_top = kwargs['top']
    chart.use(Legend(tags, top=t_top))
    # 添加工具栏
    chart.use(Toolbox())
    # 设置绘图区域的位置，默认上留120， 下留100
    chart.use(Grid())
    # tooltip
    chart.use(Tooltip())
    # 返回数据
    return chart.get_opt()


# 画图
def client_perf_draw_lines(filelist):
    if not filelist:
        return False

    cpu_datas = OrderedDict()
    mem_datas = OrderedDict()
    batter_datas = OrderedDict()
    net_datas = OrderedDict()
    montior_time_line = list()
    batter_time_line = list()
    net_time_line = list()
    json_data = list()

    # 如果有同种数据文件，说明要进行多数据对比，同名就再加上日期信息
    batter_files = fuzzy_match(filelist, 'BatterInfo')
    monitor_files = fuzzy_match(filelist, 'MonitorInfo')
    net_files = fuzzy_match(filelist, 'NetInfo')

    for file in filelist:
        temp_list = file.split('_')
        filename = temp_list[1]
        file_data = data_clean(file)
        # 识别是电量文件，从中获取耗电量
        if file.find('BatterInfo') != -1:
            batter_datas[filename] = file_data[1]
            if len(file_data[0]) > len(batter_time_line):
                batter_time_line = file_data[0]

        # 识别是监控文件，从中获取CPU和内存数据
        elif file.find('MonitorInfo') != -1:
            cpu_datas[filename] = file_data[2]
            mem_datas[filename] = file_data[1]
            if len(file_data[0]) > len(montior_time_line):
                montior_time_line = file_data[0]

        # 识别是网络文件，从中获取流量
        elif file.find('NetInfo') != -1:
            net_datas[filename+'_total'] = scale_list(file_data[1], '', -1048576)
            net_datas[filename+'_up'] = scale_list(file_data[3], '', -1048576)
            net_datas[filename+'_down'] = scale_list(file_data[2], '', -1048576)
            if len(file_data[0]) > len(net_time_line):
                net_time_line = file_data[0]

    # 绘制cpu曲线图
    if monitor_files:
        json_data.append(draw(cpu_datas,
        title='CPU占用曲线图',
        subtext='数据源:%s' % scale_list(monitor_files, 'uploads/', None),
        label=['time', '%', montior_time_line]))

    # 绘制内存曲线图
        json_data.append(draw(mem_datas,
        title='内存占用曲线图',
        subtext='数据源:%s' % scale_list(monitor_files, 'uploads/', None),
        label=['time', 'MB', montior_time_line]))

    # 绘制电量曲线图
    if batter_datas:
        json_data.append(draw(batter_datas,
        title='电量消耗曲线图',
        subtext='数据源:%s' % scale_list(batter_files, 'uploads/', None),
        label=['time', '%', batter_time_line]))

    # 绘制流量曲线图
    if net_datas:
        json_data.append(draw(net_datas,
        title='流量消耗曲线图',
        subtext='数据源:%s' % scale_list(net_files, 'uploads/', None),
        label=['time', 'MB', net_time_line]))

    return json_data


if __name__ == '__main__':
    pass