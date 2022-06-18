import logging

from db import db

log = logging.getLogger(__name__)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    @classmethod
    def find_by_id(cls, id):
        log.debug("Find product by id:{}".format(id))
        return cls.query.get(id)

    @classmethod
    def find_all(cls):
        log.debug("Find all products")
        return cls.query.all()

    def save_to_db(self):
        log.debug("Save product to database: id={}, name={}".format(self.id, self.name))
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        log.debug(
            "Delete product from database: id={}, name={}".format(self.id, self.name)
        )
        db.session.delete(self)
        db.session.commit()

    @property
    def json(self):
        data = {"id": self.id, "name": self.name}

        return data
