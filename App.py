from asyncio.windows_events import NULL
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
from app.Models.User import User, user_schema, users_schema

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

PHOTO, FIRSTNAME, LASTNAME, MOBILE, LOCATION, BIO = range(6)

validation = {
    'first_name': 'لطفا نام خود را وارد کنید',
    'last_name': 'لطفا نام خانوگی خود را وارد کنید',
    'mobile': 'لطفا شماره موبایل خود را وارد کنید',
    'age': 'لطفا سن خود را وارد کنید',
    'state': 'لطفا نام استان محل زندگی خود را وارد کنید',
    'city': 'لطفا نام شهر خود را وارد کنید',
    'photo': 'لطفا تصویر پروفایل خود را وارد کنید',
}

logger = logging.getLogger(__name__)
token = "2016260844:AAGwWwI6ZLA7cLUNNcAbbFz2W84wkJebZyo"
user = User()
isUser = []
def start(update, context):
    username = update.message.from_user
    user.username = username
    logger.info("Name of User is %s", username)
    update.message.reply_text(validation['first_name'])
    return FIRSTNAME

def first_name(update, context):
    first_name = update.message.text
    user.first_name = first_name
    isUser.append(first_name)
    logger.info("your first_name is %s", first_name)
    update.message.reply_text(validation['last_name'])
    return LASTNAME

def last_name(update, context):
    last_name = update.message.text
    user.last_name = last_name
    isUser.append(last_name)
    logger.info("your last_name is %s", last_name)
    logger.info("users array is %s", isUser)
    update.message.reply_text(validation['mobile'])
    return MOBILE


    db.session.add(user)
    db.session.commit()

def phone_number(update, context):
    phone_number = update.message.text
    user.last_name = phone_number
    isUser.append(phone_number)
    logger.info("your phone_number is %s", first_name)
    update.message.reply_text()
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

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    app.run(debug=True)


