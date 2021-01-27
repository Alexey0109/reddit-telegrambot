import config
from config import TOKEN as main_token
from config import DEVTOKEN as report_token
from config import TESTTOKEN as debug_token
from prawcore.exceptions import Forbidden
import praw
import random
import telebot
import json

def getPosts(sub):
    app_id = config.appid
    secret = config.secret
    reddit = praw.Reddit(client_id=app_id,
                     client_secret=secret,
                     user_agent=config.praw_useragent)
    submission = reddit.subreddit(sub).random()
    return submission

def NSFW(id, flag):
    with open('json/filters.json', 'r') as f:
        data = json.load(f)
    if id not in data:
        data[id] = {}
    data[id]['NSFW'] = str(flag)
    with open('json/filters.json', 'w') as f:
        json.dump(data, f, indent = 4)

def add_sub(subreddit):
    with open('json/stats.json', 'r') as f:
        data = json.load(f)
    if subreddit not in data['stats']:
        data['stats'][subreddit] = 0
    data['stats'][subreddit] = str(int(data['stats'][subreddit]) + 1)
    with open('json/stats.json', 'w') as f:
        json.dump(data, f, indent = 4)
