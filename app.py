# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2017-1-25 11:01:39
# Author     : cc
# Description:


from shutil import move
from flask import Flask, render_template, url_for, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from func import *

ALLOWED_EXTENSIONS = set(['txt', 'csv', 'html', 'jpg', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # print(request.form)
        if 'draw_server_performance' in request.form:
            file_names = ''
            for key in request.form:
                if key.find('_stat') != -1 and key.endswith('.csv'):
                    if file_names == '':
                        file_names = os.path.basename(key)
                    else:
                        file_names = file_names + '&' + os.path.basename(key)
            if file_names != '':
                return redirect(url_for('server_performance', filenames=file_names))
            else:
                return '<h1>请选中文件</h1>'

        elif 'draw_client_x9_loadscenes' in request.form:
            file_names = ''
            for key in request.form:
                if key.endswith('.log'):
                    if file_names == '':
                        file_names = os.path.basename(key)
                    else:
                        file_names = file_names + '&' + os.path.basename(key)
            if file_names != '':
                return redirect(url_for('x9_client_loadscenes', filenames=file_names))
            else:
                return '<h1>请选中文件</h1>'

        elif 'draw_client_performance' in request.form:
            file_names = ''
            for key in request.form:
                if key.endswith('.txt'):
                    if file_names == '':
                        file_names = os.path.basename(key)
                    else:
                        file_names = file_names + '&' + os.path.basename(key)
            if file_names != '':
                return redirect(url_for('client_performance', filenames=file_names))
            else:
                return '<h1>请选中文件</h1>'

        # 上传文件
        elif request.files['file']:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect('/')

    file_list = get_filelist_timerank('uploads')
    return render_template('index.html', folder=file_list)


# 上传目录文件列表
@app.route('/uploads/<filename>')
def uploads(filename):
    if filename.find('_stat') != -1 and filename.endswith('.csv'):
        nlist = list()
        nlist.append('uploads/' + filename)
        chart_datas = server_perf_draw_lines(nlist)
        return render_template('charts.html', chart_opts=chart_datas)
    else:
        file_path = 'uploads/' + filename
        f = open(file_path, 'r')
        text = ''
        for line in f.readlines():
            text = line + text
        f.close()
        return '<h1>%s</h1>' % text


# 回收站目录文件列表
@app.route('/recycled/<filename>', methods=['GET', 'POST'])
def recycled(filename='index'):
    if filename == 'index':
        file_list = get_filelist_timerank('recycled')
        return render_template('recycled.html', folder=file_list)
    else:
        file_path = 'recycled/' + filename
        f = open(file_path, 'r')
        text = ''
        for line in f.readlines():
            text = line + text
        f.close()
        return '<h1>%s</h1>' % text


# 将上传目录的文件移入回收站
@app.route('/recycle_file/<filename>')
def recycle_file(filename):
    f1 = 'uploads/%s' % filename
    f2 = 'recycled/%s' % filename
    move(f1, f2)
    return redirect('/')


# 将回收站的文件还原到上传目录
@app.route('/restore_file/<filename>')
def resotre_file(filename):
    f1 = 'uploads/%s' % filename
    f2 = 'recycled/%s' % filename
    move(f2, f1)
    return redirect('/recycled/index')


# 从回收站真实删除文件
@app.route('/delete_file/<filename>')
def delete_file(filename):
    os.remove('recycled/'+filename)
    return redirect('/recycled/index')


# 下载文件
@app.route('/download_file/<filename>')
def download_file(filename):
    return send_from_directory('uploads', filename, as_attachment=True)


# 绘制服务端性能测试数据曲线图
@app.route('/server_performance/<filenames>')
def server_performance(filenames):
    file_list = filenames.split('&')
    for i in range(0, len(file_list)):
        file_list[i] = 'uploads/' + file_list[i]
    chart_datas = server_perf_draw_lines(file_list)
    return render_template('charts.html', chart_opts=chart_datas)


# 绘制x9项目客户端场景加载时长柱状图
@app.route('/x9_client_loadscenes/<filenames>')
def x9_client_loadscenes(filenames):
    file_list = filenames.split('&')
    for i in range(0, len(file_list)):
        file_list[i] = 'uploads/' + file_list[i]
    chart_datas = client_x9_load_scenes_draw_bar(file_list)
    return render_template('charts.html', chart_opts=chart_datas)


# 绘制客户端性能测试数据曲线图
@app.route('/client_performance/<filenames>')
def client_performance(filenames):
    file_list = filenames.split('&')
    for i in range(0, len(file_list)):
        file_list[i] = 'uploads/' + file_list[i]
    chart_datas = client_perf_draw_lines(file_list)
    return render_template('charts.html', chart_opts=chart_datas)


# 获取文件上传时间
@app.context_processor
def context_upload_time():
    def upload_time(filename):
        return time.strftime('%Y-%m-%d %H:%M', time.localtime(get_mtime(filename)))
    return dict(upload_time=upload_time)


# 截取文件名
@app.context_processor
def context_cut_filename():
    def cut_filename(filename):
        return os.path.basename(filename)
    return dict(cut_filename=cut_filename)


# 判断是否是可上传文件
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run('100.84.47.220')

