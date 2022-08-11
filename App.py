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
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler, ContextTypes
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
from eyed3 import load
from stepic import encode
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TT2, TIT2, TPE1, TRCK, TALB, USLT, error
from mutagen.easyid3 import EasyID3
import locale
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

BUTTON, FIRSTNAME, LASTNAME, MOBILE, AGE, STATE, CITY, PHOTO, AUDIO, LANG, BIO = range(11)

logger = logging.getLogger(__name__)
token = "2016260844:AAGwWwI6ZLA7cLUNNcAbbFz2W84wkJebZyo"
user = User()
isUser = []
s = []
photo_file = ''
audio_file = ''
app_language = ''
my_lang = 'Please select your language'

validation = {
    'first_name': 'لطفا نام خود را وارد کنید',
    'last_name': 'لطفا نام خانوگی خود را وارد کنید',
    'mobile': 'لطفا شماره موبایل خود را وارد کنید',
    'age': 'لطفا سن خود را وارد کنید',
    'state': 'لطفا نام استان محل زندگی خود را وارد کنید',
    'city': 'لطفا نام شهر خود را وارد کنید',
    'photo': 'لطفا تصویر خود را وارد کنید',
    'audio': 'لطفا موزیک خود را وارد کنید',
    'thank_you': 'از شما متشکریم',
    'bio': 'bio',
}

validation1 = [
    {
        'first_name_en': 'Please enter your name',
        'last_name_en': 'لطفا نام خانوگی خود را وارد کنید',
        'mobile_en': 'لطفا شماره موبایل خود را وارد کنید',
        'age_en': 'لطفا سن خود را وارد کنید',
        'state_en': 'لطفا نام استان محل زندگی خود را وارد کنید',
        'city_en': 'لطفا نام شهر خود را وارد کنید',
        'photo_en': 'Please enter your image',
        'audio_en': 'Please enter your music',
        'thank_you_en': 'از شما متشکریم',
        'bio_en': 'bio',
        'first_name_fa': 'لطفا نام خود را وارد کنید',
        'last_name_fa': 'لطفا نام خانوگی خود را وارد کنید',
        'mobile_fa': 'لطفا شماره موبایل خود را وارد کنید',
        'age_fa': 'لطفا سن خود را وارد کنید',
        'state_fa': 'لطفا نام استان محل زندگی خود را وارد کنید',
        'city_fa': 'لطفا نام شهر خود را وارد کنید',
        'photo_fa': 'لطفا تصویر خود را وارد کنید',
        'audio_fa': 'لطفا موزیک خود را وارد کنید',
        'thank_you_fa': 'از شما متشکریم',
        'bio_fa': 'bio',
    }
]

def localization(validation, app_language):
    return {
        "first_name": validation['first_name_' + app_language],
        "last_name": validation['last_name_' + app_language],
        "mobile": validation['mobile_' + app_language],
        "age": validation['age_' + app_language],
        "city": validation['city_' + app_language],
        "photo": validation['photo_' + app_language],
        "audio": validation['audio_' + app_language],
        "thank_you": validation['thank_you_' + app_language],
        "bio": validation['bio_' + app_language],
    }

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

cancle = [
    KeyboardButton("cancle"), 
]

langs = [
    [
        InlineKeyboardButton("فارسی", callback_data="fa"), 
        InlineKeyboardButton("english", callback_data="en"),
    ]
]

def start(update, context):
    # reply_markup = InlineKeyboardMarkup(langs)
    # logger.info("your langugage is %s", langs)
    # update.message.reply_text(my_lang, reply_markup=reply_markup)
    # return LANG
    username = update.message.from_user
    user.user_info = username
    user.username = username.username
    logger.info("Name of User is %s", username)
    update.message.reply_text(validation['photo'])
    return PHOTO

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

def phone_number(update, context):
    phone_number = update.message.text
    user.phone_number = phone_number
    isUser.append(phone_number)
    logger.info("your phone_number is %s", phone_number)
    reply_markup = InlineKeyboardMarkup(ages)
    update.message.reply_text(validation['age'], reply_markup=reply_markup)
    return AGE

def age(update, context) -> None:
    query = update.callback_query
    query.answer()
    user.age = {query.data}
    isUser.append(query.data)
    logger.info("your age is %s", {query.data})
    reply_markup = InlineKeyboardMarkup(states)
    query.edit_message_text(validation['state'], reply_markup=reply_markup)
    return STATE

def state(update, context):
    query = update.callback_query
    query.answer()
    user.state = {query.data}
    isUser.append(query.data)
    logger.info("your state is %s", {query.data})
    reply_markup = InlineKeyboardMarkup(cities)
    query.edit_message_text(validation['city'], reply_markup=reply_markup)
    return CITY

def city(update, context):
    query = update.callback_query
    query.answer()
    user.city = {query.data}
    isUser.append(query.data)
    logger.info("your city is %s", {query.data})
    query.edit_message_text(validation['photo'])
    return PHOTO

def lang(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    app_language = query.data
    # locale.setlocale(locale.LC_ALL, app_language)
    logger.info("your lang is %s", app_language)
    # logger.info("your lang type is %s", type(app_language))
    query.edit_message_text(localization('photo', app_language))
    return PHOTO

def photo(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.png')
    logger.info(user)
    # reply_markup = ReplyKeyboardMarkup(
    #     keyboard=cancel, 
    #     resize_keyboard=True, 
    #     input_field_placeholder="hello")
    # update.message.reply_text(validation['audio'], reply_markup=reply_markup)
    update.message.reply_text(validation['audio'])
    return AUDIO

def audio(update: Update, context: CallbackContext) -> None:
    audio_file = update.message.audio.get_file()
    audio_file.download('user_music.mp3')

    pic_file = 'user_photo.png'
    audio = MP3('user_music.mp3', ID3=ID3)    
 
 # در صورتی که عکس دارای تگ باشد آن را حذف میکند
    id3 = ID3('user_music.mp3')
    if id3.getall('APIC'):
        audio.delete()
        audio.save()

    try:
        audio.add_tags()
    except:
        pass
    
    audio.tags.add(APIC(
        encoding=3,
        mime='image/png',
        type=3,
        desc='Cover Picture',
        data=open(pic_file, 'rb').read()
    ))
    audio.tags.add(TT2(encoding=3, text='salam doste man'))
    audio.tags.add(TALB(encoding=3, text='album'))
    audio.save()

    logger.info(audio)

    chat_id = update.message.chat_id
    context.bot.send_document(chat_id, document=open('user_music.mp3', 'rb'))
    return ConversationHandler.END

def bio(update, context):
    user = update.message.from_user
    logger.info("your FirstName is %s, and your LastName is %s, and your PhoneNumber is %s, and your Age is %s, and your State is %s, and your City is %s", 
    user.first_name, user.last_name, user.phone_number, user.age, user.state, user.city)
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

def echo(update, context):
    update.message.reply_text('چی میگی')

def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRSTNAME: [MessageHandler(Filters.text, first_name)],
            LASTNAME: [MessageHandler(Filters.text, last_name)],
            MOBILE: [MessageHandler(Filters.text, phone_number)],
            AGE: [CallbackQueryHandler(age)],
            STATE: [CallbackQueryHandler(state)],
            CITY: [CallbackQueryHandler(city)],
            PHOTO: [MessageHandler(Filters.photo, photo)],
            AUDIO: [MessageHandler(Filters.audio, audio)],
            LANG: [CallbackQueryHandler(lang)],
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


