from config import app
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler, ContextTypes
from telegram import Update
from telegram import (
    InlineKeyboardButton, 
    ReplyKeyboardMarkup, 
)
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TT2, TALB
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
    # tt2 = audio["TT2"].text[0] #tt2


    audio = ID3('user_music.mp3')
    
    # logger.info("Artist: %s" % audio['TPE1'].text[0])
    # logger.info("Track: %s" % audio["TIT2"].text[0])
    # logger.info("Release Year: %s" % audio["TDRC"].text[0])

    # s = ["Artist: ", "Track: ", "Release Year"]



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



    s = ''

    if audio.getall('TPE1') == [audio['TPE1']]:
        s += "Artist: " + audio["TPE1"].text[0] + "\n"
        # artsit = "your Artist: " + artist

    if audio.getall('TIT2') == [audio['TIT2']]:
        s += "Track: " + audio["TIT2"].text[0] + "\n"

    # if audio.getall('TDRC') == [audio['TDRC']]:
    #     s.append("Release Year" + audio["TDRC"].text[0])

    # artist = audio['TPE1'].text[0]
    # track = audio["TIT2"].text[0]
    # release_year = audio["TDRC"].text[0]
    update.message.reply_text(s)
    # Artist = audio['TPE1'].text[0] #Artist
    # Track = audio["TIT2"].text[0] #Track 
    # Release = audio["TDRC"].text[0] #Release
    # Release = audio["TDRC"].text[0] #Release


    # logger.info("your Artist is %s", Artist)
    # logger.info("your Track is %s", Track)
    # logger.info("your Release is %s", Release)
    
 # در صورتی که عکس دارای تگ باشد آن را حذف میکند
    # id3 = ID3('user_music.mp3')
    # if id3.getall('APIC'):
    #     audio.delete()
    #     audio.save()

    # try:
    #     audio.add_tags()
    # except:
    #     pass
    
    # audio.tags.add(APIC(
    #     encoding=3,
    #     mime='image/png',
    #     type=3,
    #     desc='Cover Picture',
    #     # data=open(pic_file, 'rb').read()
    #     data=open(pic_file, encoding='ISO-8859-1').read().encode()
    # ))
    # audio.tags.add(TT2(encoding=3, text='سلام مصطفی حالت چطوره'))
    # audio.tags.add(TALB(encoding=3, text='album'))
    # audio.save()

    # id3 = ID3('user_music.mp3')
    # tt2 = id3["TT2"].text[0] #tt2
    # logger.info("your tt2 is %s", tt2)

    # # logger.info(audio)

    # chat_id = update.message.chat_id
    # context.bot.send_document(chat_id, document=open('user_music.mp3', 'rb'))
    # # context.bot.send_document(chat_id, tags)
    # update.message.reply_text(tt2)
    # return PHOTO

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
