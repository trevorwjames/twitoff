"""
Main app/routing file for TwitOff
"""
from flask import Flask, render_template
from twitoff.models import DB, User
from twitoff.twitter import insert_example_user


def create_app():
    """create and configure an instance of the application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    # ...TODO make the app!
    @app.route('/')
    def root():
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/update')
    def update():
        # reset the database
        insert_example_user()
        return render_template('base.html', title='Users Updated!', users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset database')

    @app.route('/trevor')
    def trevor():
        hi = 'Hello Human, I am Trevor THE creator of TwitOff, well at least this version of twitoff...' \
             'designed by Lambda School, with a walkthrough by Aaron Gallant, and with lots of help from ' \
             'my TL Broken, and all my fellow students...'
        return hi

    return app
