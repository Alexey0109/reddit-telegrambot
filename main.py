import praw
import random
import telebot

token = '910437898:AAE9pmyFTMwATIsmXcNPVBv2z9SdP3nz_WA'
bot = telebot.TeleBot(token)

subreddit = None

def getPosts(sub):
    app_id = 'Vlu73kg2jM6Ueg'
    secret = 'YB7yFBbo67SlXo44x9hNG7Ae0Kc'
    reddit = praw.Reddit(client_id=app_id,
                     client_secret=secret,
                     user_agent='testscript')
    print(reddit)
    i = 0
    urls = {}
    for submission in reddit.subreddit(sub).new(limit=25):
        urls[i] = submission.url
        i += 1
    n = random.randint(0, 25)
    if n == 25: n - 1
    print(n, end=': ')
    print(urls[n])
    return urls[n]

@bot.message_handler(commands=['start'])
def StartReply(message):
    bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(content_types=['text'])
def GetSub(message):
    try:
        subreddit = message.text[1:]
        bot.send_message(message.chat.id, "Please, wait...")
        post_url = getPosts(subreddit)
        bot.send_message(message.chat.id, post_url)
    except:
        bot.send_message(message.chat.id, "Seems like no such subreddit")
bot.polling()