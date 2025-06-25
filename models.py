from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class HardwareItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100))
    serial = db.Column(db.String(100))
    location = db.Column(db.String(100))
    status = db.Column(db.String(50))
    custom_type_detail = db.Column(db.String(100))

