import pymongo
import pandas as pd
import re

from selenium_img import manhuatai
from flask import (
    Flask, request, render_template, jsonify,
    session
)

app = Flask(__name__)


# 连接数据库
client = pymongo.MongoClient('localhost', 27017)
db = client['shujus']  # 获取数据库
table = db['data_chapter']  # 获取表


@app.route('/')
@app.route('/<title>')
def view_index(title=''):
    page = request.values.get('page', '')
    name = request.values.get('searchkey', '')
    # import ipdb; ipdb.set_trace()
    # 读取数据
    data = pd.DataFrame(list(table.find()))
    _set = set()
    if page == '':
        page = 1
    page = int(page)
    for j, i in data.iterrows():
        for j in i['_type'].split(' '):
            _set.add(j)
    # pandas 模糊查询
    if name != '':
        r = ['\\w*' + i for i in name if i != ' ']
        r.append('\\w*')
        r = ''.join(r)
        data_r = pd.DataFrame()
        for j, i in data.iterrows():
            if re.match(r, i['name']):
                data_r = data_r.append(i, ignore_index=True)
        data = data_r
    # import ipdb; ipdb.set_trace()

    try:
        title_data = pd.DataFrame()
        if title == '':
            return render_template('/home/sort.html', data=data.loc[(page-1)*10:page*10-1], _set=_set, shu=int(len(data)/10), yei=[page, title])
        else:
            for j, i in data.iterrows():
                if title in i['_type']:
                    title_data = title_data.append(i,ignore_index=True)
            return render_template('/home/sort.html', data=title_data.loc[(page-1)*10:page*10-1], _set=_set,  shu=int(len(title_data)/10), yei=[page, title])
    except TypeError:
        return render_template('/home/no.html', _set=_set)

        

@app.route('/detailed/<name>')
def view_detailed(name=''):
    data = table.find_one({'name': name})
    data['chapter'] = eval(data['chapter'])
    return render_template('/home/details.html', data=data)


@app.route('/selenium', methods=['GET', 'POST'])
def view_selenium():
    _url = request.values.get('but_url', None)
    yc = request.values.get('yc', None)
    list_x = yc.split(',')
    data = table.find_one({'name': list_x[1]})
    chapter = eval(data['chapter'])
    zhang = {
        'san_zhan': None,
        'xia_zhan': None
    }
    for i, v in enumerate(chapter):
        if i == int(list_x[0]) - 1:
            zhang['san_zhan'] = [chapter[v], int(list_x[0]) - 1]
        elif i == int(list_x[0]) + 1:
            zhang['xia_zhan'] = [chapter[v], int(list_x[0]) + 1]
        elif i == int(list_x[0]):
            z = v
    # import ipdb; ipdb.set_trace()
    data_url = manhuatai(_url)
    return render_template('/home/content.html', data_url=data_url, **zhang, name=list_x[1], z=z)


if __name__ == '__main__':
    app.run(
        # host='0.0.0.0',
        debug=True
    )
