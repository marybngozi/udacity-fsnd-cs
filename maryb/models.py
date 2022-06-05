from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    team_id = db.Column(db.Integer, ForeignKey('teams.id'), nullable=True)

    def format(self):
        return {
            'name': self.firstname + self.lastname,
            'id': self.id
        }


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    persons = db.relationship('Person', backref="team", lazy=True)

    def format(self):
        return {
            'name': self.name,
            'id': self.id,
        }
