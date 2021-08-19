"""Retrieve tweets and users, then create embeddings to populate our database"""
from os import getenv
import tweepy
import spacy
import models
import en_core_web_sm
import os

nlp = spacy.load("my_model")

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH) 

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector
    
def add_or_update_user(username):
    try:
        twitter_user = TWITTER.get_user(username)
        db_user =  (models.User.query.get(twitter_user.id)) or models.User(id=twitter_user.id, name= username)
        models.db.session.add(db_user)

        tweets = twitter_user.timeline(
            count=200, exclude_replies= True, include_rts = False,
            tweet_mode = "Extended")
    
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            vectorized_tweet = vectorize_tweet(tweet.text)
            db_tweet= models.Tweet(id= tweet.id, text = tweet.text,
            vect = vectorized_tweet)
            db_user.tweets.append(db_tweet)
        
    
        models.db.session.commit()
    except Exception as e:
        print('Error processing{}: {}'.format(username,e))
        raise e
