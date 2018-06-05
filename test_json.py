import json


class User():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @property
    def json(self):
        return {"id": self.id, "name": self.name}


# json转换器（对象转成json对象的字符）
# 作用： 将字典对象转成json字符串
# import json
# json.dumps(obj, cls=XxxJSONEncoder)
class UserEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, User):
            return json.dumps(o.json)
        return json.JSONEncoder.default(self, o)


users = [User(1,'disen'), User(2,'Jack'),User(3,'Citi')]
json_str = json.dumps(users, cls= UserEncoder)
print(json_str)