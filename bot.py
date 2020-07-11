import telebot
import process
import os
from PIL import Image

token = '1263539510:AAGuCrDHx4C1DY_kVg7aFDRhFT1uZHHbCN0'
bot = telebot.TeleBot(token)


def dell_all():
    os.remove('frame_done.png')
    os.remove('1_done.png')
    os.remove('2_done.png')
    os.remove('3_done.png')
    os.remove('1.png')
    os.remove('2.png')
    os.remove('3.png')


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.text == "/start":
        bot.send_message(message.chat.id, 'Send me some document(photo), but first send me some msg(text)')


@bot.message_handler(content_types=['text'])
def do_text(message):
    global input_str
    input_str = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    text = message.text
    array = process.parse_string(text)
    main_text = process.hlwn(array)
    text = main_text + process.find_hashtags(main_text)
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['document'])
def do_photo(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        with open('frame.png', 'wb') as new_file:
            bot.send_chat_action(message.chat.id, 'typing')
            new_file.write(downloaded_file)
            size = process.get_img_size('frame.png')

        process.cut_png(size)
        process.do_image_png(input_str=input_str, switcher='hlwn')

        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_photo(message.chat.id, open('frame_done.png', 'rb'))

        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_photo(message.chat.id, open('1_done.png', 'rb'))

        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_photo(message.chat.id, open('2_done.png', 'rb'))

        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_photo(message.chat.id, open('3_done.png', 'rb'))

        dell_all()

    except Exception as ex:
        bot.send_message(message.chat.id, "[!] error - {}".format(str(ex)))


bot.polling()