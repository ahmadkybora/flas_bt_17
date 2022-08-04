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
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

BUTTON, FIRSTNAME, LASTNAME, MOBILE, AGE, STATE, CITY, PHOTO, AUDIO, BIO = range(10)

validation = {
    'first_name': 'لطفا نام خود را وارد کنید',
    'last_name': 'لطفا نام خانوگی خود را وارد کنید',
    'mobile': 'لطفا شماره موبایل خود را وارد کنید',
    'age': 'لطفا سن خود را وارد کنید',
    'state': 'لطفا نام استان محل زندگی خود را وارد کنید',
    'city': 'لطفا نام شهر خود را وارد کنید',
    'photo': 'لطفا تصویر پروفایل خود را وارد کنید',
    'audio': 'لطفا موزیک خود را وارد کنید',
    'thank_you': 'از شما متشکریم',
    'bio': 'bio'
}

logger = logging.getLogger(__name__)
token = "2016260844:AAGwWwI6ZLA7cLUNNcAbbFz2W84wkJebZyo"
user = User()
isUser = []
s = []
photo_file = ''
audio_file = ''

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
    user.user_info = username
    user.username = username.username
    logger.info("Name of User is %s", username)
    update.message.reply_text(validation['first_name'])
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

def photo(update, context):
    # user = update.message.from_user
    first_name = update.message.text
    # photo_file = update.message.photo[-1].get_file()
    # photo_file.download('user_photo.jpg')
    # s.append(photo_file)
    logger.info(user)
    # db.session.add(user)
    # db.session.commit()
    # logger.info("your FirstName is %s, and your LastName is %s, and your PhoneNumber is %s, and your Age is %s, and your State is %s, and your City is %s", 
    # user.first_name, user.last_name, user.phone_number, user.age, user.state, user.city)
    # update.message.reply_text(
    #     'thank you for login'
    # )
    update.message.reply_text(validation['audio'])
    return AUDIO

def audio(update: Update, context: CallbackContext) -> None:
    # user = update.message.from_user
    first_name = update.message.text
    # audio_file = update.message.audio.get_file()
    # audio_file.download('user_music.mp3')
    # s.append(audio_file)
    # new_file = context.bot.get_file(file_id=update.message.audio.file_id)
    # new_file.download()

    # new_file = context.bot.get_file(update.message.voice)
    # new_file = update.message.audio
    # logger.info(new_file)
    # new_file.download(f"voice_note.ogg")

    # logger.info(user)
    # db.session.add(user)
    # db.session.commit()
    # logger.info("your FirstName is %s, and your LastName is %s, and your PhoneNumber is %s, and your Age is %s, and your State is %s, and your City is %s", 
    # user.first_name, user.last_name, user.phone_number, user.age, user.state, user.city)
    # update.message.reply_text(
    #     'thank you for login'
    # )
    # chat_id = update.message.chat_id
    # document = open('user_photo.jpg', 'rb')
    # context.bot.send_document(chat_id, document)


    # data = "this is The Secret Data ha ha ha  haaaaaa. https://mrpython.blog.ir"

    # audio = input("Audio : ")
    # img_name = input("Image : ")
    # audio = load(audio) # Opening the audio file

    # img = Image.open(img_name)
    # img_steg = encode(img , data.encode()) # Encode data into Image
    # img_steg.save(img_name) # save encoded image

    # audio.initTag()
    # audio.tag.images.set(3 , open(img_name,"rb").read() , "image/png") # set cover to audio file
    # audio.tag.save() # save changes in audio file

    # print("ok") # The END :)
    # input()

    data = "سلام مصطفی جون"

    photo_file = 'user_photo.jpg'
    audio_file = 'user_music.mp3'
    audio_file = load(audio_file)
    # chat_id = update.message.chat_id
    # context.bot.send_document(chat_id, document=open(audio_file, 'rb'))
    # context.bot.send_photo(chat_id, photo=open(photo_file, 'rb'))

    # img_steg = encode(image , data.encode()) # Encode data into Image
    # img_steg.save(image) # save encoded image

    img = Image.open(photo_file)
    img_steg = encode(img , data.encode())
    img_steg.save(photo_file)

    audio_file.initTag()
    audio_file.tag.images.set(3 , open(photo_file,"rb").read() , "image/jpg") # set cover to audio file
    audio_file.tag.save() # save changes in audio file
    logger.info(audio_file)

    chat_id = update.message.chat_id
    context.bot.send_document(chat_id, document=open(audio_file, 'rb'))

    # document = open('user_photo.jpg', 'rb')
    # audio.download('user_tag_music.mp3')

    # context.bot.send_document(chat_id, audio_file)

    # new_file = context.bot.get_file(file_id=audio)
    # new_file.download()
    
    # update.message.reply_text(validation['bio'])
    return BIO

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
            # PHOTO: [MessageHandler(Filters.photo, photo)],
            # AUDIO: [MessageHandler(Filters.audio, audio)],
            PHOTO: [MessageHandler(Filters.text, photo)],
            AUDIO: [MessageHandler(Filters.text, audio)],
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


