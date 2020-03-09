import praw
import random
import telebot

#token = '966351011:AAGDUmgrpOfujpT5flyRlOn26Li-_U8f7Dg'
#Testbot token
token = '910437898:AAE9pmyFTMwATIsmXcNPVBv2z9SdP3nz_WA'
bot = telebot.TeleBot(token)

subreddit = None

FFILTER = {}
SOURCE = {}
NSFW = {}

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
    global NSFW, SOURCE, FFILTER
    bot.send_message(message.chat.id, "Hello!")
    NSFW[message.chat.id] = '0'
    FFILTER[message.chat.id] = '0'
    SOURCE[message.chat.id] = '0'
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
                urls[i] = submission.url
                i += 1
            post_url = urls[num]
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
    bot.send_message(message.chat.id, "No such files. Try again")
def Filter(message):
    global FFILTER, SOURCE
    source = SOURCE[message.chat.id]
    content_filter = FFILTER[message.chat.id]
    try:
        subreddit = message.text[1:]
        #bot.send_message(message.chat.id, "Please, wait...")
        post = getPosts(subreddit).url
        post_url = post.url
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
        elif(content_filter == 'gfy'):
            src = post_url[8:18]
            if(src=='gfycat.com'):
                bot.send_message(message.chat.id, post_url)
            else: last(message)
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
    
@bot.message_handler(content_types=['text'])
def GetSub(message):
    global FFILTER, SOURCE, NSFW
    content_filter = FFILTER[message.chat.id]
    source = SOURCE[message.chat.id]
    over18 = NSFW[message.chat.id]
    print(str(len(source)))
    try:
        subreddit = message.text[1:]
        bot.send_message(message.chat.id, "Please, wait...")
        post = getPosts(subreddit)
        post_url = post.url
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
        bot.send_message(message.chat.id, "Seems like no such subreddit")
        print(e)
bot.polling()