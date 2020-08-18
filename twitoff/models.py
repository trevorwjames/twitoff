"""
SQLAlchemy models and utility functions for TwitOff
"""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twittter users corresponding to their tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    # tweets are ordinal objects so we can fetch new tweets
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '-User {}-'.format(self.name)


class Tweet(DB.Model):
    """Tweet test and data"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # Allows for text + links
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)
