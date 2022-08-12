from config.database import app
from dataclasses import field
from config import app
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
from eyed3 import load
from stepic import encode
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TT2, TIT2, TPE1, TRCK, TALB, USLT, error
from mutagen.easyid3 import EasyID3
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

PHOTO, AUDIO = range(2)

logger = logging.getLogger(__name__)
token = "2016260844:AAGwWwI6ZLA7cLUNNcAbbFz2W84wkJebZyo"
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

# cancle = [
#     KeyboardButton("cancle"), 
# ]

reply_keyboard = [
    ["Cancel"],
]
cancle = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

langs = [
    [
        InlineKeyboardButton("فارسی", callback_data="fa"), 
        InlineKeyboardButton("english", callback_data="en"),
    ]
]

def start(update: Update, context: CallbackContext):
    # reply_markup = InlineKeyboardMarkup(langs)
    # logger.info("your langugage is %s", langs)
    # update.message.reply_text(my_lang, reply_markup=reply_markup)
    # return LANG
    username = update.message.from_user
    logger.info("Name of User is %s", username)
    update.message.reply_text(validation['photo'])
    return PHOTO

def photo(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.png')
    # reply_markup = ReplyKeyboardMarkup(
    #     keyboard=cancel, 
    #     resize_keyboard=True, 
    #     input_field_placeholder="hello")
    update.message.reply_text(validation['audio'], reply_markup=cancle)
    # update.message.reply_text(validation['audio'])
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
    audio.tags.add(TT2(encoding=3, text='سلام مصطفی حالت چطوره'))
    audio.tags.add(TALB(encoding=3, text='album'))
    audio.save()

    logger.info(audio)

    chat_id = update.message.chat_id
    context.bot.send_document(chat_id, document=open('user_music.mp3', 'rb'))
    update.message.reply_text(validation['photo'])
    return PHOTO

def cancel(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info("name of user is %s", username)
    update.message.reply_text('متشکریم از شما %s', username)
    return ConversationHandler.END

    # user = update.message.from_user
    # logger.info("name of user is %s", user.first_name)
    # update.message.reply_text(
    #     'send me a photo of yourself, '
    #     'so that we can register you, or send /skip if you don\'t want to.',
    #     reply_markup=ReplyKeyboardRemove(),
    # )
    # return ConversationHandler.END

def echo(update, context):
    update.message.reply_text('مصطفی چی میگی نمیفهمم')

def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PHOTO: [MessageHandler(Filters.photo, photo)],
            AUDIO: [MessageHandler(Filters.audio, audio)],
        },
        fallbacks = [MessageHandler(Filters.text("Cancel"), cancel)],
        # fallbacks = [CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    # dispatcher.add_handler(MessageHandler(Filters.text("Cancel"), cancel))
    # dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    app.run(debug=True)
