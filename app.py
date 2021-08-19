import os
from flask import Flask, render_template, request, jsonify, flash, redirect, Blueprint
import models
from flask_sqlalchemy import SQLAlchemy
import twitter
import predict
from dotenv import load_dotenv
load_dotenv()

def create_app():

    app = Flask(__name__)
    admin_routes = Blueprint("admin_routes", __name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    models.db.init_app(app)
    @app.route("/", methods=["GET", "POST"])
    def root():
        models.db.create_all()
        return render_template("base.html", title="home", users = models.User.query.all())

    @app.route('/update')
    def update():
        models.insert_example_users()
        return render_template('base.html', users = models.User.query.all())    
    
    @app.route('/reset')
    def reset():
        models.db.drop_all()
        models.db.create_all()
        return render_template('base.html', title= "Reset")
    
    @app.route('/user', methods = ['GET', 'POST'])
    def user():
        twitter.add_or_update_user(request.form['user_name'])
        return render_template('base.html', title = "User", users = models.User.query.all())

    @app.route('/compare', methods = ['GET', 'POST'])
    def compare():
        user1, user2 = sorted(
            [request.values['user1'], request.values['user2']]
        )
        if user1 == user2:
            message = "Cannot compare the same user"
        else:
            prediction = predict.predict_user(
                user1, user2, request.values['tweet_text'])
            message = "'{}' is more likely to be tweeted by {} than {}.".format(
                request.values['tweet_text'],
                user2 if prediction == [1,] else user1,
                user1 if prediction == [1,] else user2
            )
            return render_template("results.html", title = "prediction", message= message)
    return app
