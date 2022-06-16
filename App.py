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
inlineKeys = [
    [InlineKeyboardButton('1', url='google.com', callback_data='1'), InlineKeyboardButton('2', url='google.com')], 
    [InlineKeyboardButton('3', url='google.com'), InlineKeyboardButton('4', url='google.com'), InlineKeyboardButton('5', url='google.com')], 
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
    update.effective_message.reply_text('12', reply_markup=markup)

    # btnMarkup = ReplyKeyboardMarkup(
    #     keyboard=btnKey, 
    #     resize_keyboard=True, 
    #     input_field_placeholder="hello")

    # update.message.reply_text(lorem, reply_markup=btnMarkup)
    # inlineMarkup = InlineKeyboardMarkup(inlineKeys)
    # update.message.reply_text(lorem, reply_markup=inlineMarkup)

def echo(update, context):
    update.message.reply_text('ho')
    # update.message.reply_text('h', reply_markup=ReplyKeyboardRemove)

def login(update, context):
    update.message.reply_text('login')

def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("login", login))
    dispatcher.add_handler(MessageHandler(Filters.text("b"), echo))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    # main()
    app.run(debug=True)