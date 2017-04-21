#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2017-1-23 15:52:37
# Author     : cc
# Description: get data from file

import os
import csv
import time


# 获取指定目录及其子目录下（所有或指定类型'log,txt'）的文件
def get_files(path, types=None, svn_file=False):
    type_files = list()
    for root, dirs, allfiles in os.walk(path):
        # 过滤掉svn隐藏文件
        if not svn_file:
            if root.find('.svn') != -1:
                continue
        if allfiles:
            for name in allfiles:
                file = '%s/%s' % (root, name)
                file = file.replace('\\', '/').replace('//', '/')
                file = file.split('/')[-1]
                if types is not None:
                    type_list = types.split(',')
                    end_text = os.path.splitext(name)[-1].replace('.', '')
                    if end_text not in type_list:
                        continue
                type_files.append(file)

    return type_files


# 获取最大值max、最小值min、中位值median或平均值average
def count_list(oldlist):
    arr = sorted(oldlist)
    data = dict()
    size = len(arr)
    half = size // 2

    data['max'] = arr[-1]
    data['min'] = arr[0]
    data['median'] = (arr[half] + arr[~half]) / 2
    data['average'] = round(sum(arr) / size, 2)

    return data


# 将cvs文件里的数据按行读取
def csv_list(csv_file):
    with open(csv_file, 'rt') as rf:
        reader = csv.reader(rf)
        rows = [row for row in reader]
        return rows


# 遍历list元素，去掉指定字符串并将数值缩放
def scale_list(oldlist, cut=' ', deno=1):
    datalist = oldlist[:]
    size = len(datalist)
    for i in range(size):
        if type(datalist[i]) == str:
            datalist[i] = datalist[i].replace(',', '').replace(cut, '').replace(' ','')
        if deno == None:
            continue
        elif deno > 0:
            datalist[i] = round(float(datalist[i]) * deno, 2)
        elif deno < 0:
            temp = -deno
            datalist[i] = round(float(datalist[i]) / temp, 2)
        else:
            datalist[i] = round(float(datalist[i]), 2)

    return datalist


# 遍历list的值，累积相加变成新的list，例如：[1,2,3]→[1,3,6]
def cumprod_list(oldlist):
    num_list = oldlist[:]
    size = len(num_list)
    count = 0
    for i in range(size):
        num_list[i] = round(count + num_list[i], 2)
        count = num_list[i]

    return num_list


# 将两个list的值分别进行相加
def add_counter_list(*oldlists):
    current_list = list()
    for oldlist in oldlists:
        cur_len = len(current_list)
        old_len = len(oldlist)
        if cur_len < old_len:
            for i in range(old_len - cur_len):
                current_list.append(0)

        for j in range(len(current_list)):
            assert oldlist[j], 'list index out of range'
            current_list[j] = round(current_list[j] + float(oldlist[j]), 2)

    return current_list


# 获取文件的修改时间
def get_mtime(file):
    return os.stat(file).st_mtime


# 获取目录下的所有文件，并按时间从新到旧排序
def get_filelist_timerank(path=''):
    file_list = os.listdir(path)
    new_list = list()

    for file in file_list:
        local_path = os.path.join(path, file)
        if os.path.isfile(local_path):
            new_list.append(local_path)

    return sorted(new_list, key=get_mtime, reverse=True)


# 模糊匹配list中元素个数
def count_fuzzy_match(nlist, b_str):
    num = 0
    for item in nlist:
        if item.find(b_str) != -1:
            num = num + 1
    return num


# 模糊匹配list中的元素，并返回列表
def fuzzy_match(nlist, b_str):
    rlist = list()
    for item in nlist:
        if item.find(b_str) != -1:
            rlist.append(item)
    return rlist


if __name__ == '__main__':
    a = ''
    print(len(a))


