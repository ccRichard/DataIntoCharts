# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2017-2-6 18:00:30
# Author     : cc
# Description:


import sys
from collections import OrderedDict

from func.common import *

sys.path.append('../')
from echarts import Echart, Legend, Line, Axis, Tooltip, Toolbox, Grid


# 从sys_stat.csv文件中获取数据
def sys_data_clean(file):
    # dstat记录的数据前5行为冗余数据，第6行为表头
    data_list = csv_list(file)[5:]
    data_dict = OrderedDict()
    headers = data_list[0]
    for header in headers:
        data_dict[header] = list()

    for data in data_list[1:]:
        for index, value in enumerate(headers):
            try:
                data_dict[value].append(data[index])
            except:
                data_dict[value].append(0)
    return data_dict


# 从process_stat.csv文件中获取多个进程的数据
def process_data_clean(file):
    # dstat记录的数据前5行为冗余数据，第6行为表头
    data_list = csv_list(file)[5:]
    data_dict = OrderedDict()
    headers = data_list[0]
    pid_index = headers.index('pid')

    for data in data_list[1:]:
        process_id = data[pid_index]
        if process_id not in data_dict:
            data_dict[process_id] = OrderedDict()
            for header in headers:
                data_dict[process_id][header] = list()

        for index, value in enumerate(headers):
            try:
                data_dict[process_id][value].append(data[index])
            except:
                data_dict[process_id][value].append(0)
    return data_dict


# 绘图
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
    x_line = []
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
    # 设置绘图区域的位置，默认上留120，下留100
    chart.use(Grid())
    # tooltip
    chart.use(Tooltip())
    # 打开浏览器并绘图
    # chart.plot()
    return chart.get_opt()


# 画图
def server_perf_draw_lines(filelist):
    if not filelist:
        return False

    cpu_datas = OrderedDict()
    mem_datas = OrderedDict()
    io_datas = OrderedDict()
    flow_datas = OrderedDict()
    time_line = list()
    json_data = []

    # 系统或进程文件的数量影响到线条命名的方式
    # 例如只有一个sys文件，可以直接用system命名，但如果有2个以上，就需要区分为system1和system2
    sys_num = count_fuzzy_match(filelist, 'sys_stat')
    process_num = count_fuzzy_match(filelist, 'process_stat')

    for file in filelist:
        # 识别是系统文件
        if file.find('sys_stat') != -1:
            filename = 'system'
            if sys_num > 1:
                filename = filename + file.split('sys_stat')[-1].replace('.csv', '')

            # 获取列表数据
            sys_data = sys_data_clean(file)
            time_line = sys_data['time']
            cpu_datas[filename] = add_counter_list(sys_data['usr'], sys_data['sys'])
            mem_datas[filename] = scale_list(sys_data['used'], '', -1048576)
            io_datas[filename+'_read'] = scale_list(sys_data['read'], '', -1024)
            io_datas[filename+'_write'] = scale_list(sys_data['writ'], '', -1024)
            flow_datas[filename+'_recv_ps'] = scale_list(sys_data['recv'], '', -1048576)
            flow_datas[filename+'_send_ps'] = scale_list(sys_data['send'], '', -1048576)
            # 流量累计增长数值
            flow_datas[filename+'_recv_total'] = cumprod_list(flow_datas[filename+'_recv_ps'])
            flow_datas[filename+'_send_total'] = cumprod_list(flow_datas[filename+'_send_ps'])

        # 识别是进程文件
        elif file.find('process_stat') != -1:
            filename = ''
            if process_num > 1:
                filename = file.split('process_stat')[-1].replace('.csv', '')

            # 获取列表数据
            process_datas = process_data_clean(file)
            for key in process_datas:
                p_data = process_datas[key]
                p_name = '%s%s%s' % (p_data['name'][0], key, filename)
                p_line = p_data['time']
                if len(p_line) > len(time_line):
                    time_line = p_line

                cpu_datas[p_name] = p_data['cpu']
                mem_datas[p_name] = scale_list(p_data['mem'], '', -1048576)
                io_datas[p_name+'_read'] = scale_list(p_data['io_read'], '', -1024)
                io_datas[p_name+'_write'] = scale_list(p_data['io_write'], '', -1024)

        # 其他文件不处理
        else:
            return False

    # 绘制cpu曲线图
    json_data.append(draw(cpu_datas,
        title='CPU占用曲线图',
        subtext='数据源:%s' % scale_list(filelist, 'uploads/', None),
        label=['time', '%', time_line]))

    # 绘制内存曲线图
    json_data.append(draw(mem_datas,
         title='内存占用曲线图',
         subtext='数据源:%s' % scale_list(filelist, 'uploads/', None),
         label=['time', 'MB', time_line]))

    # 绘制IO曲线图
    json_data.append(draw(io_datas,
         title='IO曲线图',
         subtext='数据源:%s' % scale_list(filelist, 'uploads/', None),
         label=['time', 'kb', time_line]))

    # 绘制流量曲线图
    if flow_datas:
        json_data.append(draw(flow_datas,
             title='流量曲线图',
             subtext='数据源:%s' % scale_list(filelist, 'uploads/', None),
             label=['time', 'MB', time_line]))

    return json_data


if __name__ == '__main__':
    pass



