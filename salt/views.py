from pyramid.view import view_config
import praw
import threading
import time
import random

last_fetch = 0
cached_subs = []
refresh_time = 60 * 10
phrases = [
"Putting the lit in Politics.",
"It's AirBnB meets Monsanto.",
"Pure ingredients.  Finest Quality.  Imported from California.",
"The most useless thing on the internet.",
"You know you have a drinking problem when the bartender knows your name -- and you've never been to that bar before."
]

def shouldFetch():
    global last_fetch
    global refresh_time
    return last_fetch < time.time() - refresh_time;

def fetchSubReddits():
    global cached_subs
    global last_fetch
    if shouldFetch():
      last_fetch = time.time()
      numToFetch = 10
      subReddits = ['liberal', 'conservative', 'libertarian', 'progressive']
      r = praw.Reddit(user_agent='test_reddit_app')
      submissions = []
      for subReddit in subReddits:
        submissions.extend([s for s in r.get_subreddit(subReddit).get_hot(limit=numToFetch)])
      random.shuffle(submissions)
      cached_subs = submissions

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    global cached_subs
    if shouldFetch():
        t = threading.Thread(target=fetchSubReddits)
        t.start()
    return {'subs' : cached_subs, 'phrase': random.choice(phrases)}
