import praw
import random
import telebot

#token = '966351011:AAGDUmgrpOfujpT5flyRlOn26Li-_U8f7Dg'
#Testbot token
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

content_filter = None

@bot.message_handler(commands=['getsource'])
def getsrc(message):
    f = open('source.txt', 'r')
    src = f.readline()
    bot.send_message(message.chat.id, src)

@bot.message_handler(commands=['source'])
def source(message):
    bot.send_message(message.chat.id, 'Source URL: ')
    bot.register_next_step_handler(message, SetSource)

def SetSource(message):
    f = open('source.txt', 'w')
    src = message.text
    if(src.lower() != 'all'):
        f.write(src.lower())
    else: f.write('0')
    bot.send_message(message.chat.id, 'Success!')

@bot.message_handler(commands=['getfilter'])
def getfilter(message):
    f = open('filter.txt', 'r')
    ff = f.readline()
    bot.send_message(message.chat.id, '*.' + ff)

@bot.message_handler(commands=['start'])
def StartReply(message):
    bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(commands=['filter'])
def SetFilterInit(message):
    bot.send_message(message.chat.id, "Type file format:")
    bot.register_next_step_handler(message, SetFilter)

def SetFilter(message):
    f = open('filter.txt', 'w')
    if(message.text.lower() == 'all'):
        f.write('0')
    else: f.write(message.text.lower())
    bot.send_message(message.chat.id, "Success!")

def last(message):
    for num in range(24):
        f = open('filter.txt', 'r')
        content_filter = f.readline()
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
    f = open('filter.txt', 'r')
    ff = open('source.txt', 'r')
    source = ff.readline()
    content_filter = f.readline()
    try:
        subreddit = message.text[1:]
        #bot.send_message(message.chat.id, "Please, wait...")
        post_url = getPosts(subreddit)
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
    f = open('filter.txt', 'r')
    content_filter = f.readline()
    ff = open('source.txt', 'r')
    source = ff.readline()
    print(str(len(source)))
    try:
        subreddit = message.text[1:]
        bot.send_message(message.chat.id, "Please, wait...")
        post_url = getPosts(subreddit)
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
    except:
        bot.send_message(message.chat.id, "Seems like no such subreddit")
bot.polling()