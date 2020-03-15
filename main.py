import praw
import random
import telebot
import sys

#token = '966351011:AAGDUmgrpOfujpT5flyRlOn26Li-_U8f7Dg'
#Testbot token
token = '910437898:AAE9pmyFTMwATIsmXcNPVBv2z9SdP3nz_WA'

# TODO:
# add flair filter
# add displaying of flair


devt = '1115795697:AAF83mMjCPWWJ8mTPAMMbWcz3fdamomOs2w'

bot = telebot.TeleBot(token)
logger = telebot.TeleBot(devt)
ID = 527294873

subreddit = None

FFILTER = {}
SOURCE = {}
NSFW = {}
FLAIR = {}
TOP_SUBS = {}

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
        urls[i] = submission
        i += 1
    n = random.randint(0, 25)
    if n == 25: n - 1
    print(n, end=': ')
    print(urls[n])
    return urls[n]

content_filter = None

@bot.message_handler(commands=['sub_rating'])
def getrate(message):
    global TOP_SUBS
    try:
        #print("RATING!")
        report = " "
        for i in sorted (TOP_SUBS, key=TOP_SUBS.get, reverse=True) :  
            if(TOP_SUBS[i] != 0):
                report += (str(i) + " rating: " + str(TOP_SUBS[i]) + '\n') 
        bot.send_message(message.chat.id, "SUBREDDIT RATING:\n" + report)
    except:
        logger.send_message(ID, "@" + message.chat.username + " | error: " + str(sys.exc_info()[0]))
@bot.message_handler(commands=['top_sub'])
def gettop(message):
    global TOP_SUBS
    try:
        bot.send_message(message.chat.id, "Current top subreddit - " + str(max(TOP_SUBS, key=TOP_SUBS.get)) + " gets " + str(TOP_SUBS[max(TOP_SUBS, key=TOP_SUBS.get)]) + " requests")
    except:
        logger.send_message(ID, "@" + message.chat.username + " | error: " + str(sys.exc_info()[0]))

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Try https://telegra.ph/Methods-Documentation-03-10\nStill have questions? Text @KeyboardDestroyer")

@bot.message_handler(commands=['nsfw_filter'])
def setover18(message):
    bot.send_message(message.chat.id, 'Display NSFW? (y/n)')
    bot.register_next_step_handler(message, setOver18)

def setOver18(message):
    global NSFW
    if(message.text.lower() == 'y'):
        NSFW[message.chat.id] = '1'
        bot.send_message(message.chat.id, 'NSFW filter was set to 1')
    else:
        NSFW[message.chat.id] = '0'
        bot.send_message(message.chat.id, 'NSFW filter was set to 0')

@bot.message_handler(commands=['getnsfw_filter'])
def getnsfwfilter(message):
    try:
        global NSFW
        bot.send_message(message.chat.id, NSFW[message.chat.id])
    except:
        bot.send_message(message.chat.id, 'Specify filter first')
@bot.message_handler(commands=['getsource'])
def getsrc(message):
    try:
        global SOURCE
        src = SOURCE[message.chat.id]
        bot.send_message(message.chat.id, src)
    except:
        bot.send_message(message.chat.id, 'Specify filter first')
@bot.message_handler(commands=['source'])
def source(message):
    bot.send_message(message.chat.id, 'Source URL: ')
    bot.register_next_step_handler(message, SetSource)

def SetSource(message):
    global SOURCE
    src = message.text
    if(src.lower() != 'all'):
        SOURCE[message.chat.id] = src.lower()
    else: SOURCE[message.chat.id] = '0'
    bot.send_message(message.chat.id, 'Success!')

@bot.message_handler(commands=['getfilter'])
def getfilter(message):
    try:
        global FFILTER 
        ff = FFILTER[message.chat.id]
        bot.send_message(message.chat.id, '*.' + ff)
    except:
        bot.send_message(message.chat.id, 'Specify filter first')
@bot.message_handler(commands=['start'])
def StartReply(message):
    global NSFW, SOURCE, FFILTER, FLAIR
    #bot.send_message(message.chat.id, "Hello!")
    NSFW[message.chat.id] = '0'
    FFILTER[message.chat.id] = '0'
    SOURCE[message.chat.id] = '0'
    FLAIR[message.chat.id] = '0'
    global TOP_SUBS
    try:
        #print("RATING!")
        report = " "
        for i in sorted (TOP_SUBS, key=TOP_SUBS.get, reverse=True) :
            if(TOP_SUBS[i] != 0):
                report += (str(i) + " rating: " + str(TOP_SUBS[i]) + '\n')
        bot.send_message(message.chat.id, "Hello! Welcome to SubredditPostGetter bot! Here you can quickly get some posts from different subreddits! To get some help type /help or text @KeyboardDestroyer \nHere you can see some popular subreddits: \n" + "SUBREDDIT RATING:\n" + report)
    except:
        logger.send_message(ID, "@" + message.chat.username + " | error: " + str(sys.exc_info()[0]))

@bot.message_handler(commands=['filter'])
def SetFilterInit(message):
    bot.send_message(message.chat.id, "Type file format:")
    bot.register_next_step_handler(message, SetFilter)

def SetFilter(message):
    global FFILTER
    if(message.text.lower() == 'all'):
        FFILTER[message.chat.id] = '0'
    else: FFILTER[message.chat.id] = message.text.lower()
    bot.send_message(message.chat.id, "Success!")
    
def last(message):
    for num in range(24):
        global FFILTER, SOURCE, NSFW
        content_filter = FFILTER[message.chat.id]
        source = SOURCE[message.chat.id]
        try:
            subreddit = message.text[1:]
            sub = subreddit
            #bot.send_message(message.chat.id, "Please, wait...")
            app_id = 'Vlu73kg2jM6Ueg'
            secret = 'YB7yFBbo67SlXo44x9hNG7Ae0Kc'
            reddit = praw.Reddit(client_id=app_id,
                                 client_secret=secret,
                                 user_agent='testscript')
            print(reddit)
            i = 0
            urls = {}
            for submission in reddit.subreddit(sub).new(limit=25):
                urls[i] = submission
                i += 1
            post_url = urls[num].title + "\n[" + str(urls[num].link_flair_text) + "]\n" + urls[num].url
            #bot.send_message(message.chat.id, post_url)
            fileformat = post_url[-3:]
            sourceurl = post_url[:len(source)]
            if(source != '0'):
                if(sourceurl != source):
                    continue
            if(content_filter == '0'):
                bot.send_message(message.chat.id, post_url)
            elif(content_filter == 'gfy'):
                src = post_url[8:18]
                if(src=='gfycat.com'):
                    bot.send_message(message.chat.id, post_url)
                    return
                else: print('err')#bot.send_message(message.chat.id, "No such files. Try again")
            elif(content_filter == 'text'):
                if(post_url[-4] != '.'):
                    bot.send_message(message.chat.id, post_url)
                    return
                else:
                    print('err')#bot.send_message(message.chat.id, "No such files. Try again")
            elif(fileformat == content_filter):
                bot.send_message(message.chat.id, post_url)
                return
            else:
                print('err')#bot.send_message(message.chat.id, "No such files. Try again")
        except Exception as ex:
            print('Fatal: ' + str(ex))#bot.send_message(message.chat.id, "Seems like no such subreddit")
            logger.send_message(ID, "@" + message.chat.username + " | error: " + str(sys.exc_info()[0]))
    bot.send_message(message.chat.id, "No such files. Try again")
def Filter(message):
    global FFILTER, SOURCE
    try:
        source = SOURCE[message.chat.id]
        content_filter = FFILTER[message.chat.id]
        subreddit = message.text[1:]
        #bot.send_message(message.chat.id, "Please, wait...")
        post = getPosts(subreddit)
        post_url = post.title + "\n[" + str(post.link_flair_text) + "]\n" + post.url
        #bot.send_message(message.chat.id, post_url)
        if (post.over_18):
            if(over18 == '0'):
                bot.send_message(message.chat.id, 'NSFW Detected! Please, try again or disable nsfw filter')
                return
        fileformat = post_url[-3:]
        sourceurl = post_url[:len(source)]
        if(source != '0'):
            if(sourceurl != source):
                Filter()
                return
        if(content_filter == '0'):
            bot.send_message(message.chat.id, post_url)
        elif(content_filter == 'text'):
            if(post_url[-4] != '.'):
                bot.send_message(message.chat.id, post_url)
            else:
                last(message)
        elif(fileformat == content_filter):
            bot.send_message(message.chat.id, post_url)
        else:
            last(message)
    except Exception as ex:
        bot.send_message(message.chat.id, str(ex))
        print(ex)
@bot.message_handler(content_types=['text'])
def GetSub(message):
    global FFILTER, SOURCE, NSFW, TOP_SUBS
    try:
        TOP_SUBS[message.text] += 1
        print(TOP_SUBS[message.text])
    except:
        TOP_SUBS[message.text] = 1
    try:
        content_filter = FFILTER[message.chat.id]
        source = SOURCE[message.chat.id]
        over18 = NSFW[message.chat.id]
    except:
        bot.send_message(message.chat.id, 'Please, restart a bot')
        logger.send_message(ID, "@" + message.chat.username + " | error: " + str(sys.exc_info()[0]))
        return
    print(str(len(source)))
    try:
        subreddit = message.text[1:]
        bot.send_message(message.chat.id, "Please, wait...")
        post = getPosts(subreddit)
        post_url = post.title + "\n[" + str(post.link_flair_text) + "]\n" + post.url
        #bot.send_message(message.chat.id, post_url)
        if (post.over_18):
            if(over18 == '0'):
                bot.send_message(message.chat.id, 'NSFW Detected! Please, try again or disable nsfw filter')
                return
        #bot.send_message(message.chat.id, post_url)
        fileformat = post_url[-3:]
        sourceurl = post_url[:len(source)]
        if(source != '0'):
            if(sourceurl != source): 
                Filter()
                return
        if(content_filter == '0'):
            bot.send_message(message.chat.id, post_url)
        elif(content_filter == 'gfy'):
            src = post_url[8:18]
            if(src=='gfycat.com'):
                bot.send_message(message.chat.id, post_url)
            else: Filter(message)
        elif(content_filter == 'text'):
            if(post_url[-4] != '.'):
                bot.send_message(message.chat.id, post_url)
            else:
                Filter(message)
        elif(fileformat == content_filter):
            bot.send_message(message.chat.id, post_url)
        else:
            Filter(message)
    except Exception as e:
        bot.send_message(message.chat.id, "Seems like no such subreddit. Try again")
        print(e)
        logger.send_message(ID, "@" + message.chat.username + " | error: " + str(sys.exc_info()[0]))
        TOP_SUBS[message.text] -= 1
bot.polling()
logger.polling()