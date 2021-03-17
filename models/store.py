
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # **NOTE** VIP - (POS1) If we remove lazy='dynamic', as soon as the, as soon as
    # we initialize the StoreModel (through __init__()), it's going to look for
    # all the items that have a relationship with this store and going to populate
    # the items' property with the list of those items.
    # If we add lazy='dynamic', then it makes the 'items' a query so that we
    # need to use self.items.all() to fetch those items.
    #
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        # **NOTE** s08e06-added 'id': self.id,
        return {'id': self.id, 'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
