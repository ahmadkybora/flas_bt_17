from config import app
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler, ContextTypes
from telegram import Update
from telegram import (
    InlineKeyboardButton, 
    ReplyKeyboardMarkup, 
)
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TT2, TALB
from mutagen.easyid3 import EasyID3
import eyed3
# import music_tag
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

PHOTO, AUDIO, = range(2)

logger = logging.getLogger(__name__)

# token = "2016260844:AAGwWwI6ZLA7cLUNNcAbbFz2W84wkJebZyo" #@bot_project_1_bot
# token = "2092105489:AAEHfZCr6xX5y4S3Bn4v0tVZJLIiND4t0NE" #@bot_project_2_bot
# token = "537716476:AAF15wE57CU2P5AuRhYps9EWW2sX_YQXf0o" #@Arkanir_bot:
# token = "434941139:AAG1Apadczm8qIT9AzT-E3BLRI9_wRIZtd4" #@yehamzabon_bot
token = "378545358:AAHuQjkYspm0CYr-ZG9xF_h31CB7V-pF118" #@Mynameisahmad_bot
# token = "353909760:AAEvjTzsEpcW3XjMcFwtMFvPh6qE1g3nszk" #@SaffronHajahmad_bot

validation = {
    'first_name': 'لطفا نام خود را وارد کنید',
    'last_name': 'لطفا نام خانوگی خود را وارد کنید',
    'mobile': 'لطفا شماره موبایل خود را وارد کنید',
    'age': 'لطفا سن خود را وارد کنید',
    'state': 'لطفا نام استان محل زندگی خود را وارد کنید',
    'city': 'لطفا نام شهر خود را وارد کنید',    
    'photo': 'لطفا تصویر خود را وارد کنید',
    'audio': 'لطفا موزیک خود را وارد کنید',
    'thank_you': 'از شما متشکریم فایل شما آماده دانلود است در ضمن میتوانید دوباره این کار ها را انجام دهید',
    'bio': 'bio',
}

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
    username = update.message.from_user
    logger.info("Name of User is %s", username)
    update.message.reply_text(validation['audio'])
    return AUDIO

def audio(update: Update, context: CallbackContext):
    global audio_file
    audio_file = update.message.audio.get_file()
    audio_file.download('user_music.mp3')
    update.message.reply_text(validation['photo'])
    return PHOTO

def photo(update: Update, context: CallbackContext):
    global photo_file
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.png')

    audio = MP3('user_music.mp3', ID3=ID3)   

    id3 = ID3('user_music.mp3')
    if id3.getall('APIC'):
        audio.save()

    try:
        audio.add_tags()
    except:
        pass
    
    audio.tags.add(APIC(
        encoding=3,
        mime='image/png',
        type=3,
        desc=u'Cover',
        data=open('user_photo.png', 'rb').read()
    ))

    audio.save(v2_version=3)

    chat_id = update.message.chat_id
    context.bot.send_document(
        chat_id, 
        document=open('user_music.mp3', 'rb'), 
        caption='the video', 
        thumb=open('user_photo.png', 'rb').read()
    )
    update.message.reply_text(validation['thank_you'])
    update.message.reply_text(validation['audio'])
    return AUDIO


    update.message.reply_text(validation['thank_you'])
    return LABEL

def cancel(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info("name of user is %s", username)
    update.message.reply_text('متشکریم از شما %s', username)
    return ConversationHandler.END

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
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(MessageHandler(Filters.text("Cancel"), cancel))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    app.run(debug=True)
