from config import app
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler, ContextTypes
from telegram import Update
from telegram import (
    InlineKeyboardButton, 
    ReplyKeyboardMarkup, 
)
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TT2, TALB
from mutagen.easyid3 import EasyID3
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

PHOTO, AUDIO = range(2)

logger = logging.getLogger(__name__)
# token = "2016260844:AAGwWwI6ZLA7cLUNNcAbbFz2W84wkJebZyo"
token = "2092105489:AAEHfZCr6xX5y4S3Bn4v0tVZJLIiND4t0NE"

validation = {
    'first_name': 'لطفا نام خود را وارد کنید',
    'last_name': 'لطفا نام خانوگی خود را وارد کنید',
    'mobile': 'لطفا شماره موبایل خود را وارد کنید',
    'age': 'لطفا سن خود را وارد کنید',
    'state': 'لطفا نام استان محل زندگی خود را وارد کنید',
    'city': 'لطفا نام شهر خود را وارد کنید',
    'photo': 'لطفا تصویر خود را وارد کنید',
    'audio': 'لطفا موزیک خود را وارد کنید',
    'thank_you': 'از شما متشکریم فایل شما آماده دانلود است در ضمن میتوانید دوباره این کار ها را انجام دهید پس لطفا تصویر خود را وارد کنید',
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
    update.message.reply_text(validation['photo'])
    return PHOTO

def photo(update: Update, context: CallbackContext):
    global photo_file
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.png')
    update.message.reply_text(validation['audio'])
    return AUDIO

def audio(update: Update, context: CallbackContext) -> None:
    global audio_file
    audio_file = update.message.audio.get_file()
    audio_file.download('user_music.mp3')

    pic_file = 'user_photo.png'
    audio = MP3('user_music.mp3', ID3=ID3)  

    audio = ID3('user_music.mp3')
    tags = audio.pprint()

    # for key in EasyID3.valid_keys.keys():
    #     update.message.reply_text(key)
    # id3 = ID3()
    # id3.add(TRCK(encoding=3, text=str(info['track'])))
    # id3.add(TDRC(encoding=3, text=str(info['year'])))
    # id3.add(TIT2(encoding=3, text=info['song_name']))
    # id3.add(TALB(encoding=3, text=info['album_name']))
    # id3.add(TPE1(encoding=3, text=info['artist_name']))
    # id3.add(TPOS(encoding=3, text=str(info['cd_serial'])))
    # lyric_data = self.get_lyric(info)
    # id3.add(USLT(encoding=3, text=lyric_data)) if lyric_data else None
    # #id3.add(TCOM(encoding=3, text=info['composer']))
    # #id3.add(WXXX(encoding=3, desc=u'xiami_song_url', text=info['song_url']))
    # #id3.add(TCON(encoding=3, text=u'genre'))
    # #id3.add(TSST(encoding=3, text=info['sub_title']))
    # #id3.add(TSRC(encoding=3, text=info['disc_code']))
    # id3.add(COMM(encoding=3, desc=u'Comment', \
    #     text=info['comment']))
    # id3.add(APIC(encoding=3, mime=u'image/jpeg', type=3, \
    #     desc=u'Front Cover', data=self.get_cover(info)))
    # id3.save(file_name) 

    # s = ''
    # art = audio.getall("APIC")
    # logger.info(art)
    # if audio.getall('TRCK') == [audio['TRCK']]:
    #     s += "Track Name:     " + audio["TRCK"].text[0] + "\n"

    # if audio.getall('TDRC') == [audio['TDRC']]:
    #     s += "Release Year" + audio["TDRC"].text[0] + "\n"

    # if audio.getall('TIT2') == [audio['TIT2']]:
    #     s += "Song Name: " + audio["TIT2"].text[0] + "\n"

    # if audio.getall('TALB') == [audio['TALB']]:
    #     s += "Album Name: " + audio["TALB"].text[0] + "\n"

    # if audio.getall('TPE1') == [audio['TPE1']]:
    #     s += "Artist Name: " + audio["TPE1"].text[0] + "\n"

    # if audio.getall('TPOS') == [audio['TPOS']]:
    #     s += "cd Serial: " + audio["TPOS"].text[0] + "\n"



    update.message.reply_text(tags)

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
