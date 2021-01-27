import config
import core
from config import TOKEN as main_token
from config import DEVTOKEN as report_token
from config import TESTTOKEN as debug_token
from prawcore.exceptions import Forbidden
from telebot import types
import praw
import random
import telebot
import json

#https://surik00.gitbooks.io/aiogram-lessons/content/chapter4.html

token = debug_token
bot = telebot.TeleBot(token)
logger = telebot.TeleBot(report_token)

PRICE = types.LabeledPrice(label='Support us', amount=10000)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'nsfw_y':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Displaying NSFW")
            core.NSFW(str(call.message.chat.id), True)
        if call.data == 'nsfw_n':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="NSFW is not displaying")
            core.NSFW(str(call.message.chat.id), False)

@bot.message_handler(commands=['start'])
def StartReply(message):
    bot.send_message(message.chat.id, "Hello! Welcome to SubredditPostGetter bot! Here you can quickly get some posts from different subreddits! To get some help type /help or text @KeyboardDestroyer")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "https://telegra.ph/Methods-Documentation-03-10")

@bot.message_handler(commands=['donate'])
def donate(message):
    bot.send_invoice(
        message.chat.id,
        title="Donate",
        description="Support us",
        provider_token="381764678:TEST:22066",
        currency='rub',
        photo_url="https://m.economictimes.com/thumb/msid-77139423,width-1200,height-900,resizemode-4,imgsize-245256/money-gety-2.jpg",
        photo_height=512,
        photo_width=512,
        photo_size=512,
        is_flexible=False,
        prices=[PRICE],
        start_parameter='time-machine-example',
        invoice_payload='some-invoice-payload-for-our-internal-use'
    )


@bot.message_handler(content_types=['successful_payment'])
def process_successful_payment(message):
    print('successful_payment')
    bot.send_message(message.chat.id, 'Thatk you for supporting us')

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(commands=['nsfw_filter'])
def nsfw_filter(message):
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text = 'Yes', callback_data ='nsfw_y'))
    menu.add(types.InlineKeyboardButton(text = 'No', callback_data ='nsfw_n'))
    bot.send_message(message.chat.id, text ='Display NSFW posts?', reply_markup = menu)

@bot.message_handler(commands=['top', 'top_subs'])
def get_top(message):
    respond = 'TOP SUBREDDITS:\n'
    with open('json/stats.json', 'r') as f:
        data = json.load(f)
    data = dict(sorted(data['stats'].items(), key=lambda item: item[1], reverse=True))
    for i in data.keys():
        respond += f'/{str(i)}: {data[str(i)]}\n'
    bot.send_message(message.chat.id, respond)

@bot.message_handler(content_types=['text'])
def subreddit_getpost(message):
    try: 
        with open('json/filters.json', 'r') as f:
            data = json.load(f)
        if str(message.chat.id) not in data or 'NSFW' not in data[str(message.chat.id)] or data[str(message.chat.id)]['NSFW'] == 'False':
            bot.send_message(message.chat.id, 'NSFW hidden. Use /nsfw_filter to enable')
            return
        subreddit = message.text[1:]
        bot.send_message(message.chat.id, "Please, wait...")
        post = core.getPosts(subreddit)
        post_url = post.title + "\n[" + str(post.link_flair_text) + "]\n" + post.url
        bot.send_message(message.chat.id, post_url)
        core.add_sub(subreddit)
    except Forbidden:
        bot.send_message(message.chat.id, 'prawcore.exceptions.Forbidden: 403 response: No such subreddit')
    except Exception as e:
        bot.send_message(message.chat.id, f'Unknown error: {e}')
        logger.send_message(config.adminid, f'@{message.chat.username} | {str(e)}')

bot.polling()
logger.polling()