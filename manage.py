import json

from flask import Flask, render_template, request, abort, jsonify, Response
from flask_cache import Cache
from models import init_db, User, Image, db

import settings

app = Flask(__name__)
app.config.from_object(settings.Config)

# 初始化db
init_db(app)

# 创建Cache对象
cache = Cache(app, config={
    "CACHE_TYPE": 'redis',
    "CACHE_REDIS_HOST": '10.35.163.38',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_DB': 3,
    'CACHE_KEY_PREFIX': 'music_cache'
})


@app.before_request
def descrapy():
    print('---请求前---', request.url, request.remote_addr)
    print('浏览器名称：', request.user_agent)  # 客户端代理器
    print('请求资源:', request.path)

    # user_agent = request.user_agent
    # print(user_agent.browser, user_agent.string)
    # if user_agent.browser == 'firefox':
    #     return '本站点，暂不支持', 201;

    # abort(500) 中断请求
    # return '哥们，不要爬了!'
    # 实现客户请求间隔在5秒以内 不让请求
    if not request.path.startswith('/static'):

        if cache.get(request.remote_addr):
            return '你的爬虫不low了，^_^!', 403

        # 设置缓存
        cache.set(request.remote_addr,
                  request.base_url,
                  timeout=5)


@app.route('/')
@cache.cached(timeout=30)
def home():
    print('--进入主页--')
    return render_template('home.html')


@app.route('/images/')
def images():
    # 获取当前请求的路径
    path = request.url
    # print(path)
    # 以当前请求路径作为缓存中的key，从缓存中读取key的value
    result = cache.get(path)
    # print(result)
    # 判断当前请求是否存在于缓存中
    if result:
        print('从缓存中读取的页面')
        return result

    print('－－－进入图库页面－－')
    # 缓存中不存在当前的请求页面
    result = render_template('images.html')  # 重新渲染
    # 将渲染的数据存放到缓存中
    cache.set(path, result, 30)


    return result


class Obj2JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, User):
            return o.json  # 返回 对象转换的字典

        return json.JSONEncoder.default(self, o)

@app.route('/users/')
def users():
    # return render_template('users.html', users=User.query.all())
    # return jsonify({"id":1, "name":"Disen", "phone":"1100199"})

    users = User.query.all()
    # 指定对象转成json对象的转码器

    return Response(json.dumps([user.json for user in users]),
                    content_type='application/json')

@app.route('/api/images', methods=('GET', 'POST', 'PUT', 'DELETE', 'PATCH'))
def apiImages():
    # 打开数据库的连接
    session = db.session

    # 声明 结果对象
    result = {"status": "ok"}

    print('args-->',request.args)
    print('form-->', request.form)
    if request.method == 'GET':
        images = Image.query.all()
        result['datas'] = [image.json for image in images]

    elif request.method == 'POST':
        img = Image()
        img.name = request.form.get('name')
        img.url = request.form.get('url')

        session.add(img)
        result['msg'] = "添加图片成功!"
    elif request.method == 'PUT':
        id = request.form.get('id')
        try:
            img = Image.query.get(int(id))

            img.name = request.form.get('name')

            session.add(img)

            result['id'] = id
            result['name'] = img.name
            result['msg'] = '更新的图片名成功!'

        except:
            return jsonify({"status": "fail",
                            "id": id,
                            "msg": "更新的图片不存在!"})
    elif request.method == 'PATCH':
        # 全部属性更新
        id = request.form.get('id')
        img = Image.query.get(int(id))
        img.name = request.form.get('name')
        img.url = request.form.get('url')

        session.add(img)  # 保存或更新

        result['msg'] = '图片的名称和路径更新成功!'

    elif request.method == 'DELETE':
        id = request.args.get('id')
        img = Image.query.get(int(id))

        session.delete(img)

        result['id'] = id
        result['msg'] = '删除图片成功!'

    if request.method != 'GET':
        session.commit()

    return jsonify(result)


if __name__ == '__main__':
    cache.clear()  # 清除缓存
    app.run(debug=True, port=8000)
