"""
Main app/routing file for TwitOff
"""
from flask import Flask, render_template, request
from twitoff.models import DB, User
from twitoff.twitter import insert_example_user, add_or_update_user
from twitoff.predict import predict_user


def create_app():
    """create and configure an instance of the application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User {name} successfully added!'
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = f"Error adding {name}: {e}"
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2,
                                      request.values['tweet_text'])
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction',
                               message=message)

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
             'designed by Lambda School, with a although by Aaron Gallant, and with lots of help from ' \
             'my TL Broken, and all my fellow students...'
        return hi

    return app
