"""
SQLAlchemy models and utility functions for TwitOff
"""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twittter users corresponding to their tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

    def __repr__(self):
        return '-User {}-'.format(self.name)


class Tweet(DB.Model):
    """Tweet test and data"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # Allows for text + links
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)


def insert_example_users():
    austen = User(id=1, name='austen')
    elon = User(id=2, name='elonmusk')
    trevor = User(id=3, name='TrevorJames', text='I am Better')
    DB.session.add(austen)
    DB.session.add(elon)
    DB.session.add(trevor)
    DB.session.commit()
