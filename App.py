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
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler
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

PHOTO, FIRSTNAME, LASTNAME, MOBILE, LOCATION, BIO = range(6)

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

def start1(update, context):
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

def start(update, context):
    user = update.message.from_user
    logger.info("first_name of user is %s", user.first_name)
    logger.info("last_name of user is %s", user.last_name)
    update.message.reply_text(
        'send me a photo of yourself, '
        'so that we can register you, or send /skip if you don\'t want to.',
        reply_markup=ReplyKeyboardRemove(),
    )
    return PHOTO

def first_name(update, context):
    first_name = update.message.text
    logger.info("your first_name is %s", first_name)
    update.message.reply_text(
        'please insert your last name'
    )
    return LASTNAME

def last_name(update, context):
    last_name = update.message.text
    logger.info("your last_name is %s", last_name)
    update.message.reply_text(
        'please insert your phone number'
    )
    return MOBILE

def phone_number(update, context):
    first_name = update.message.text
    logger.info("your first_name is %s", first_name)
    update.message.reply_text(
        'please insert your last name'
    )
    return LASTNAME

def photo(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'please insert your first name'
    )
    return FIRSTNAME

def skip_photo(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a photo", user.first_name)
    update.message.reply_text(
        'ok no problem! now, send me your location please, ' 'or send /skip'
    )
    return LOCATION

def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    update.message.reply_text(
        'ok, we will take this into conversation and notify' 'At last /skip'
    )
    return BIO

def skip_location(update, context):
    user = update.message.from_user
    logger.info("name of user is %s", user.first_name)
    update.message.reply_text(
        'ok no problem! At Last'
    )
    return BIO

def bio(update, context):
    user = update.message.from_user
    logger.info("review by %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'thank you'
    )
    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("name of user is %s", user.first_name)
    update.message.reply_text(
        'send me a photo of yourself, '
        'so that we can register you, or send /skip if you don\'t want to.',
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END

def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            FIRSTNAME: [MessageHandler(Filters.text, first_name)],
            LASTNAME: [MessageHandler(Filters.text, last_name)],
            MOBILE: [MessageHandler(Filters.text, phone_number)],
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks = [CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # dispatcher.add_handler(CommandHandler("start", start))

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