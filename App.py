from flask_migrate import Migrate
from routes.panel.userRoute import userRoute
from config.database import db, app
from dataclasses import field
from email.policy import default
from config import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime
from flask_cors import CORS
from requests import request
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    KeyboardButton
)

from app.Controllers.Panel.UserController import index, store, show, update, delete

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
token = "2016260844:AAGwWwI6ZLA7cLUNNcAbbFz2W84wkJebZyo"

lorem = ""
btnKey = [
    [KeyboardButton('ثبت نام'), KeyboardButton('ورود')], # row 1
    [KeyboardButton('سکه'), KeyboardButton('موقعیت')], # row 2
    [KeyboardButton('1'), KeyboardButton('زمان')], # row 3 
    [KeyboardButton('3'), KeyboardButton('4')], # row 4 
]

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Off', callback_data='press')],
])

inlineKeys = [
    [InlineKeyboardButton('ثبت نام', url='google.com', callback_data='1'), InlineKeyboardButton('ورود', url='google.com')], 
    [InlineKeyboardButton('موقعیت', url='google.com'), InlineKeyboardButton('زمان', url='google.com')], 
    [InlineKeyboardButton('درباره', url='google.com'), InlineKeyboardButton('خروج', url='google.com')], 
]

# بوسیله متد زیر میتوان به روت ها دسترسی داشت
# این روش برای استفاده از معماری ام وی سی است
app.register_blueprint(userRoute, url_prefix='/')

# @app.route('/')
# def index():
#     return "a"

def start(update, context):
    # markup = InlineKeyboardMarkup(
    #     [
    #         [InlineKeyboardButton('callbackData')], 
    #         [InlineKeyboardButton('callbackData')], 
    #         [InlineKeyboardButton('callbackData')], 
    #         [InlineKeyboardButton('callbackData')], 
    #     ] 
    # )
    # update.effective_message.reply_text('12', reply_markup=markup)

    markup = ReplyKeyboardMarkup(
        [
            [KeyboardButton('ثبت نام'), KeyboardButton('ورود')], # row 1
            [KeyboardButton('سکه'), KeyboardButton('موقعیت')], # row 2
            [KeyboardButton('1'), KeyboardButton('زمان')], # row 3 
            [KeyboardButton('3'), KeyboardButton('4')], # row 4 
        ] 
    )
    inlineMarkup = InlineKeyboardMarkup(inlineKeys)
    update.effective_message.reply_text('121', reply_markup=inlineMarkup)

    # btnMarkup = ReplyKeyboardMarkup(
    #     keyboard=btnKey, 
    #     resize_keyboard=True, 
    #     input_field_placeholder="hello")

    # update.message.reply_text(lorem, reply_markup=btnMarkup)
    # inlineMarkup = InlineKeyboardMarkup(inlineKeys)
    # update.message.reply_text(lorem, reply_markup=inlineMarkup)

# def do_something(user_input):
#     answer = "You have wrote me " + user_input
#     return answer
def register(update, context):
    # print('json file update : ' ,update)
    # print("json file bot : ', bot)
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    # phone_number = update.message.chat.phone_number
    print("chat_id : {} and firstname : {} lastname : {}  username : {}". format(chat_id, first_name, last_name , username))
    update.message.reply_text([first_name, username])

def do_something(user_input):
    return user_input

def register1(update, context):
    update.message.reply_text('لطفا نام خود را وارد کنید')
    # options = []
    # options.append(InlineKeyboardButton('لطفا نام خود را وارد کنید', callback_data='نام'))
    # reply_markup = InlineKeyboardMarkup([options])
    # update.effective_message.reply_text('1', reply_markup=reply_markup)

    # user_input = do_something(update.message.text)
    
    # if user_input != NULL:
    #     options.append(InlineKeyboardButton('لطفا نام خانوادگی خود را وارد کنید', callback_data='نام خانوادگی'))
    #     reply_markup = InlineKeyboardMarkup([options])
    #     update.effective_message.reply_text('2', reply_markup=reply_markup)
    # options = []

    # options.append(InlineKeyboardButton('Enter Name', callback_data='name'))
    # options.append(InlineKeyboardButton('Enter Age', callback_data='age'))

    # reply_markup = InlineKeyboardMarkup([options])

    # context.bot.send_message(chat_id='chat_id', text='Choose an option', reply_markup=reply_markup)
    # update.effective_message.reply_text('121', reply_markup=reply_markup)
    # user_input = update.message.text
    # update.message.reply_text(do_something(user_input))

    # dispatcher.add_handler(MessageHandler(Filters.text, echo))
    # telegram_bot.sendMessage(chat_id, 'Click to stop looping', reply_markup=keyboard)
    # update.effective_message.reply_text('121', reply_markup=keyboard)

def login(update, context):
    update.message.reply_text('ورود')

def location(update, context):
    update.message.reply_text('موقعیت')

def coin(update, context):
    update.message.reply_text('سکه')

def echo(update, context):
    update.message.reply_text('چی میگی')
    # update.message.reply_text('h', reply_markup=ReplyKeyboardRemove)

def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(MessageHandler(Filters.text("ورود"), login))
    dispatcher.add_handler(MessageHandler(Filters.text("ثبت نام"), register))
    dispatcher.add_handler(MessageHandler(Filters.text("موقعیت"), location))
    dispatcher.add_handler(MessageHandler(Filters.text("سکه"), coin))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    app.run(debug=True)