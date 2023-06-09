from config import db


class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_value = db.Column(db.Date, unique=True)


class DAMResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hour = db.Column(db.Integer)
    price = db.Column(db.Float)
    sales_volume = db.Column(db.Float)
    purchase_volume = db.Column(db.Float)
    declared_sales_volume = db.Column(db.Float)
    declared_purchase_volume = db.Column(db.Float)
    date_id = db.Column(db.Integer, db.ForeignKey('date.id'))

    date_rel = db.relationship("Date", backref=db.backref("dam_results", lazy=True))
