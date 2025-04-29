from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class Coordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    north_west_lat = db.Column(db.Float, nullable=False)
    north_west_lng = db.Column(db.Float, nullable=False)
    south_east_lat = db.Column(db.Float, nullable=False)
    south_east_lng = db.Column(db.Float, nullable=False)

    def __init__(self, north_west_lat, north_west_lng, south_east_lat, south_east_lng):
        self.north_west_lat = north_west_lat
        self.north_west_lng = north_west_lng
        self.south_east_lat = south_east_lat
        self.south_east_lng = south_east_lng
