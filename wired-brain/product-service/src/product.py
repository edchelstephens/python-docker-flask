from db import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.save()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def json(self):
        data = {"id": self.id, "name": self.name}

        return data
