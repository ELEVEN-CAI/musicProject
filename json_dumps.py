import json


class Music():  # 定义实体类
    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url

    @property
    def json(self):  # 将类对象转成字典对象
        return {"id": self.id,
                "name": self.name,
                "url": self.url}


class MyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Music):
            # 将字典对象转成json格式的字符
            return json.dumps(obj.json)
        return json.JSONEncoder.default(self, obj)


musics = [Music(1, '大海', 'http://mp3.xami/dahai.mp3'),
          Music(2, '成都', 'http://mp3.xami/chengdu.mp3')]

# cls 指定json转换器(json.JSONEncoder的子类)
json_str = json.dumps({"level": ['1', '2', '3', '4'],
                       "status": 200,
                       "msg": "请求成功", "music": Music(1, 'disne', 'xx').json}, skipkeys=False)
# json_str = json.dumps(musics, cls=MyJsonEncoder)
print(json_str)
print(json.dumps([music.json for music in musics]))
