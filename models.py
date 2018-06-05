from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    phone = db.Column(db.String(12))

    __tablename__ = 'user'

    @property
    def json(self):  # __dict__ 是类对象隐藏的属性 __slots__
        return {"id": self.id,
                "name": self.name,
                "phone": self.phone}


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    url = db.Column(db.String(200))

    __tablename__ = 'image'

    @property
    def json(self):
        return {"id": self.id,
                "name": self.name,
                "url": self.url}
