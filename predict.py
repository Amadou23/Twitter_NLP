import numpy as np
from sklearn.ensemble import RandomForestClassifier
import models
import twitter

def predict_user(user0_name, user1_name, hypo_tweet_text):
    user0 = models.User.query.filter(models.User.name == user0_name).first()
    user1 = models.User.query.filter(models.User.name == user1_name).first()
    user0_vect = np.array([tweet.vect for tweet in user0.tweets])
    user1_vect = np.array([tweet.vect for tweet in user1.tweets])
    vects = np.vstack([user0_vect, user1_vect])
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))]
    )

    hypo_vect = twitter.vectorize_tweet(hypo_tweet_text).reshape(1,-1)
    model = RandomForestClassifier().fit(vects, labels)
    
    return model.predict(hypo_vect)
    
