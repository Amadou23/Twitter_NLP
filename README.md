# Twitter_NLP

Link to Project: https://twitoff-amadou.herokuapp.com/

## ==Description==

This project integrates a number of methods in order to perform Natural Language Processing (NLP) on
live data derived from Twitter. The goal of this project is to demonstrate how NLP can be used at a basic
level to classify hypertext by which Twitter user is most likely to 'tweet' (or post) it. For this project,
Twitter API access had been granted, and implemented with the Tweepy wrapper for python.

To start, the web app is built using the Flask platform and is deployed on Heroku. For the functionality
of the project, data is extracted from Twitter using its API and the Tweepy library and is fed into SQLAlchemy 
tables. These tables which hold a variety of information we're concerned with, such as the usernames and past
tweeting data, are integrated with our PostgreSQL database. The Spacy library is then responsible for vectorizing
our tweets into components our models can operate on. Finally, a random forest classifier is tasked with 
receiving and training on these vectors.

The interface of the app is quite intuitive. There are two text boxes, one labeled "User to add" and
the other, "Tweet text to predict". The user is expected to type a name into the 'add' box, such that Tweepy
can add the respective Twitter user(s) and their tweeting data to our PostgreSQL database. Our random forest
will then train live on the inputted values. Once this has been accomplished with at least two Twitter users in the database, 
one can add text into the 'predict' box, select the two users they wish to compare and let our model produce a result.
