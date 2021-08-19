from flask_sqlalchemy import SQLAlchemy
import twitter


db = SQLAlchemy()

# Creates a 'user' table
class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True) # id as primary key
    name = db.Column(db.String(50), nullable=False) # user name
    newest_tweet_id = db.Column(db.BigInteger) #keeps track of recent tweet 
    def __repr__(self):
        return "<User: {}>".format(self.name)

# Creates a 'tweet' table
class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.Unicode(), nullable=False)    
    vect = db.Column(db.PickleType, nullable = False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)
    
def insert_example_users():
    twitter.add_or_update_user('elonmusk')
    twitter.add_or_update_user('nasa')