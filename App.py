# from asyncio.windows_events import NULL
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
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import Update
from telegram import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    KeyboardButton,
    Contact
)
from app.Models.User import User, user_schema, users_schema

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

FIRSTNAME, LASTNAME, MOBILE, AGE, STATE, CITY, PHOTO, BIO = range(8)

validation = {
    'first_name': 'لطفا نام خود را وارد کنید',
    'last_name': 'لطفا نام خانوگی خود را وارد کنید',
    'mobile': 'لطفا شماره موبایل خود را وارد کنید',
    'age': 'لطفا سن خود را وارد کنید',
    'state': 'لطفا نام استان محل زندگی خود را وارد کنید',
    'city': 'لطفا نام شهر خود را وارد کنید',
    'photo': 'لطفا تصویر پروفایل خود را وارد کنید',
    'thank_you': 'از شما متشکریم'
}

logger = logging.getLogger(__name__)
token = "2016260844:AAGwWwI6ZLA7cLUNNcAbbFz2W84wkJebZyo"
user = User()
isUser = []


ages = [
    [
        InlineKeyboardButton("18", callback_data=str("18")), 
        InlineKeyboardButton("19", callback_data="19"), 
        InlineKeyboardButton("20", callback_data="20"), 
        InlineKeyboardButton("21", callback_data="21"), 
        InlineKeyboardButton("22", callback_data="22"), 
        InlineKeyboardButton("23", callback_data="23"), 
        InlineKeyboardButton("24", callback_data="24"), 
        InlineKeyboardButton("25", callback_data="25"), 
        InlineKeyboardButton("26", callback_data="26"), 
        InlineKeyboardButton("27", callback_data="27"), 
        InlineKeyboardButton("28", callback_data="28"), 
        InlineKeyboardButton("29", callback_data="29"), 
        InlineKeyboardButton("30", callback_data="30"), 
    ],
    [
        InlineKeyboardButton("31", callback_data="31"), 
        InlineKeyboardButton("32", callback_data="32"), 
        InlineKeyboardButton("33", callback_data="33"), 
        InlineKeyboardButton("34", callback_data="34"), 
        InlineKeyboardButton("35", callback_data="35"), 
        InlineKeyboardButton("36", callback_data="36"), 
        InlineKeyboardButton("37", callback_data="37"), 
        InlineKeyboardButton("38", callback_data="38"), 
        InlineKeyboardButton("39", callback_data="39"), 
        InlineKeyboardButton("40", callback_data="40"), 
        InlineKeyboardButton("41", callback_data="41"), 
        InlineKeyboardButton("42", callback_data="42"), 
        InlineKeyboardButton("43", callback_data="43"), 
    ],
]

states = [
    [
        InlineKeyboardButton("18", callback_data="18"), 
        InlineKeyboardButton("19", callback_data="19"), 
        InlineKeyboardButton("20", callback_data="20"), 
        InlineKeyboardButton("21", callback_data="21"), 
        InlineKeyboardButton("22", callback_data="22"), 
        InlineKeyboardButton("23", callback_data="23"), 
        InlineKeyboardButton("24", callback_data="24"), 
        InlineKeyboardButton("25", callback_data="25"), 
        InlineKeyboardButton("26", callback_data="26"), 
        InlineKeyboardButton("27", callback_data="27"), 
        InlineKeyboardButton("28", callback_data="28"), 
        InlineKeyboardButton("29", callback_data="29"), 
        InlineKeyboardButton("30", callback_data="30"), 
    ],
    [
        InlineKeyboardButton("31", callback_data="31"), 
        InlineKeyboardButton("32", callback_data="32"), 
        InlineKeyboardButton("33", callback_data="33"), 
        InlineKeyboardButton("34", callback_data="34"), 
        InlineKeyboardButton("35", callback_data="35"), 
        InlineKeyboardButton("36", callback_data="36"), 
        InlineKeyboardButton("37", callback_data="37"), 
        InlineKeyboardButton("38", callback_data="38"), 
        InlineKeyboardButton("39", callback_data="39"), 
        InlineKeyboardButton("40", callback_data="40"), 
        InlineKeyboardButton("41", callback_data="41"), 
        InlineKeyboardButton("42", callback_data="42"), 
        InlineKeyboardButton("43", callback_data="43"), 
    ],
]

cities = [
    [
        InlineKeyboardButton("18", callback_data="18"), 
        InlineKeyboardButton("19", callback_data="19"), 
        InlineKeyboardButton("20", callback_data="20"), 
        InlineKeyboardButton("21", callback_data="21"), 
        InlineKeyboardButton("22", callback_data="22"), 
        InlineKeyboardButton("23", callback_data="23"), 
        InlineKeyboardButton("24", callback_data="24"), 
        InlineKeyboardButton("25", callback_data="25"), 
        InlineKeyboardButton("26", callback_data="26"), 
        InlineKeyboardButton("27", callback_data="27"), 
        InlineKeyboardButton("28", callback_data="28"), 
        InlineKeyboardButton("29", callback_data="29"), 
        InlineKeyboardButton("30", callback_data="30"), 
    ],
    [
        InlineKeyboardButton("31", callback_data="31"), 
        InlineKeyboardButton("32", callback_data="32"), 
        InlineKeyboardButton("33", callback_data="33"), 
        InlineKeyboardButton("34", callback_data="34"), 
        InlineKeyboardButton("35", callback_data="35"), 
        InlineKeyboardButton("36", callback_data="36"), 
        InlineKeyboardButton("37", callback_data="37"), 
        InlineKeyboardButton("38", callback_data="38"), 
        InlineKeyboardButton("39", callback_data="39"), 
        InlineKeyboardButton("40", callback_data="40"), 
        InlineKeyboardButton("41", callback_data="41"), 
        InlineKeyboardButton("42", callback_data="42"), 
        InlineKeyboardButton("43", callback_data="43"), 
    ],
]
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


    # db.session.add(user)
    # db.session.commit()

def phone_number(update, context):
    # contact = update.effective_message.contact
    # phone = contact.phone_number
    # phone = update.message.contact.phone_number
    # phone = update.effective_message.contact
    # contact = update.effective_message
    # phone_number = Contact(contact)
    phone_number = update.message.text
    user.last_name = phone_number
    user.mobile = phone_number
    isUser.append(phone_number)
    logger.info("your phone_number is %s", phone_number)
    reply_markup = InlineKeyboardMarkup(ages)
    update.message.reply_text(validation['age'], reply_markup=reply_markup)
    return AGE

    # age = ReplyKeyboardMarkup(
    #     [
    #         [InlineKeyboardButton(1), InlineKeyboardButton(2), InlineKeyboardButton(3), InlineKeyboardButton(4)],
    #     ] 
    # )
    # inlineMarkup = InlineKeyboardMarkup(age)
    # update.message.reply_text(age)
    # update.effective_message.reply_text('لطفا یکی را انتخاب کنید', reply_markup=inlineMarkup)

    # inlineKeys = [
    #     [InlineKeyboardButton('ثبت نام', url='google.com', callback_data='1'), InlineKeyboardButton('ورود', url='google.com')], 
    #     [InlineKeyboardButton('موقعیت', url='google.com'), InlineKeyboardButton('زمان', url='google.com')], 
    #     [InlineKeyboardButton('درباره', url='google.com'), InlineKeyboardButton('خروج', url='google.com')], 
    # ]
    # inlineMarkup = InlineKeyboardMarkup(inlineKeys)
    # update.effective_message.reply_text('121', reply_markup=inlineMarkup)


def age(update, context) -> None:
    query = update.callback_query
    # query.answer()
    user.age = query
    isUser.append(query)
    logger.info("your age is %s", age)
    reply_markup = InlineKeyboardMarkup(states)
    query.edit_message_text(validation['state'], reply_markup=reply_markup)

    # query = update.callback_query
    # query.answer()

    # age = update.callback_query.data
    # age.answer(f'selected: {age.data}')
    # age.answer()
    # age.edit_message_text(text=f"Selected option: {age.data}")

    # user.last_name = phone_number
    # isUser.append(query)
    # logger.info("your age is %s", query)
    # reply_markup = InlineKeyboardMarkup(states)
    # update.message.reply_text(validation['state'], reply_markup=reply_markup)
    return STATE

def state(update, context):
    state = update.message.text
    # user.last_name = phone_number
    isUser.append(state)
    logger.info("your state is %s", state)
    reply_markup = InlineKeyboardMarkup(cities)
    update.message.reply_text(validation['city'], reply_markup=reply_markup)
    return CITY

def city(update, context):
    city = update.message.text
    # user.last_name = phone_number
    isUser.append(city)
    logger.info("your city is %s", city)
    update.message.reply_text(validation['city'])
    return PHOTO

def photo(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'please insert your first name'
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

# def skip_photo(update, context):
#     user = update.message.from_user
#     logger.info("User %s did not send a photo", user.first_name)
#     update.message.reply_text(
#         'ok no problem! now, send me your location please, ' 'or send /skip'
#     )
#     return LOCATION

# def location(update, context):
#     user = update.message.from_user
#     user_location = update.message.location
#     logger.info("location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
#     )
#     update.message.reply_text(
#         'ok, we will take this into conversation and notify' 'At last /skip'
#     )
#     return BIO

# def skip_location(update, context):
#     user = update.message.from_user
#     logger.info("name of user is %s", user.first_name)
#     update.message.reply_text(
#         'ok no problem! At Last'
#     )
#     return BIO

# def bio(update, context):
#     user = update.message.from_user
#     logger.info("review by %s: %s", user.first_name, update.message.text)
#     update.message.reply_text(
#         'thank you'
#     )
#     return ConversationHandler.END

# def cancel(update, context):
#     user = update.message.from_user
#     logger.info("name of user is %s", user.first_name)
#     update.message.reply_text(
#         'send me a photo of yourself, '
#         'so that we can register you, or send /skip if you don\'t want to.',
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     return ConversationHandler.END

def echo(update, context):
    update.message.reply_text('چی میگی')

def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            PHOTO: [MessageHandler(Filters.photo, photo)],
            FIRSTNAME: [MessageHandler(Filters.text, first_name)],
            LASTNAME: [MessageHandler(Filters.text, last_name)],
            MOBILE: [MessageHandler(Filters.text, phone_number)],
            AGE: [CallbackQueryHandler(age)],
            # LOCATION: [
            #     MessageHandler(Filters.location, location),
            #     CommandHandler('skip', skip_location),
            # ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks = [CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    app.run(debug=True)


