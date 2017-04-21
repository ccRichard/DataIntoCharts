# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2017-2-10 16:12:33
# Author     : cc
# Description: 用于测试上传文件到flask


import requests

file = {'file': open('test1.txt', 'rb')}
try:
    r = requests.post('http://100.84.47.220:5000', files=file, timeout=10)
    print('send success')
except Exception as ex:
    print('upload failed, you can try again manually')
