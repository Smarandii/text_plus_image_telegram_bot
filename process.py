# -*- coding: <encoding name> -*-
import cv2
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def get_img_size(img_path):
    size = {}
    file = Image.open(img_path)
    size[0], size[1] = file.size
    return size


def divide_to_words_and_smb_only(s):
    symbols = [",", ":", "!", "?", " ", '', '"', "«", '»' '—', '-', '&', ' ',]
    allowed_symbols = ['.', '\n', '👥']
    w = ''
    words = []
    for i in range(len(s)):
        if s[i] in allowed_symbols:
            if w != '':
                words.append(w)
                w = ''
            words.append(s[i])

        elif s[i] in symbols:
            if w != '':
                words.append(w)
                w = ''
        else:
            w = w + s[i]
    words.append(w)
    return words


def find_hashtags(s):
    hash_tags = ''
    keywords = {'коронавирус': '#covid19 #коронавирус #коронавирус2020 #коронавирусмир #коронавируснаяинфекция #пандемия ',
                'кредит': '#кредит2020 #кредитрф ',
                'covid-19': '#covid19 #коронавирус #коронавирус2020 #коронавирусмир #коронавируснаяинфекция #пандемия ',
                'коронавирусная': '#covid19 #коронавирус #коронавирус2020 #коронавирусмир #коронавируснаяинфекция #пандемия ',
                'пандемия': '#covid-19 #коронавирус #коронавирус2020 #коронавирусмир #коронавируснаяинфекция #пандемия '}

    words = divide_to_words_and_smb_only(s)
    words.append(" ")

    for i in range(len(words)):
        if words[i].lower() in keywords and keywords[words[i].lower()] not in hash_tags:
            hash_tags += keywords[words[i].lower()]

        elif (words[i].istitle() and i != 0) and (words[i] not in hash_tags):
            if words[i - 1] != '\n':
                if words[i - 1] != '.':
                    hash_tags += f'#{words[i]}'
                    if words[i + 1].istitle():
                        hash_tags += words[i + 1]
                    if words[i + 2].istitle():
                        hash_tags += words[i + 2]
                    hash_tags += " "
                    print(hash_tags)

    return hash_tags


def cut_png(size):
    name = 'frame.png'
    width = size[0]
    height = size[1]
    r1 = (0, 0, height, height)
    r2 = (width/2 - height/2, 0, width/2 + height/2, height)
    r3 = (width - height, 0, width, height)

    img1 = Image.open(name)
    cropped_img1 = Image.Image.crop(img1, r1)
    cropped_img1.save("1.png")

    img2 = Image.open(name)
    cropped_img2 = Image.Image.crop(img2, r2)
    cropped_img2.save("2.png")

    img3 = Image.open(name)
    cropped_img3 = Image.Image.crop(img3, r3)
    cropped_img3.save("3.png")


def do_image_png(input_str, switcher='economy'):

    fonts = {'economy': 'Blogger Sans.otf',
             'minitrip': 'HelveticaNeueCyr.ttf',
             'hlwn': 'HelveticaNeueCyr.ttf'}

    font_sizes = {'economy': 65,
                  'minitrip': 60,
                  'hlwn': 60}

    sources = {'economy': 'source_economy.png',
               'minitrip': "source_minitrip.png",
               'hlwn': 'source_hlwnr.png'}

    strings = {'economy': ((70, 845), (70, 915), (70, 870)),
                'minitrip': ((70, 855), (70, 925), (70, 880)),
                'hlwn': ((70, 855), (70, 925), (70, 880))
               }

    need_to_proceed = {'economy': ['1', '2', '3'],
                       'minitrip': ['frame'],
                       'hlwn': ['1', '2', '3', 'frame']}

    source = sources[switcher]
    filename = fonts[switcher]
    kegl = font_sizes[switcher]
    font = ImageFont.truetype(filename, kegl)

    up_string, down_string, middle_string = strings[switcher]

    input_str = input_str.upper()
    words = input_str.split(" ")

    for i in need_to_proceed[switcher]:
        img_name = f"{i}.png"
        save_path = f"{i}_done.png"
        if len(input_str) < 51:
            img1 = Image.open(source).convert('RGBA')
            draw1 = ImageDraw.Draw(img1)

            if len(words) == 1:
                font = ImageFont.truetype(filename, 90)
                draw1.text(middle_string, words[0], (255, 255, 255, 255), font=font)

            elif len(words) == 2:

                draw1.text(up_string, words[0], (255, 255, 255, 255), font=font)
                draw1.text(down_string, words[1], (255, 255, 255, 255), font=font)

            elif len(words) == 3 and len(words[0] + " " + words[1]) < 25:

                draw1.text(up_string, words[0] + " " + words[1], (255, 255, 255, 255), font=font)
                draw1.text(down_string, words[2], (255, 255, 255, 255), font=font)

            elif len(words) == 4 and len(words[0] + " " + words[1]) < 25 and len(words[2] + " " + words[3]) < 25:

                draw1.text(up_string, words[0] + " " + words[1], (255, 255, 255, 255), font=font)
                draw1.text(down_string, words[2] + " " + words[3], (255, 255, 255, 255), font=font)

            elif len(words) == 5 and len(words[0] + " " + words[1] + " " + words[2]) < 25 and len(
                    words[3] + " " + words[4]) < 25:

                draw1.text(up_string, words[0] + " " + words[1] + " " + words[2], (255, 255, 255, 255), font=font)
                draw1.text(down_string, words[3] + " " + words[4], (255, 255, 255, 255), font=font)

            elif len(words) == 6 and len(words[0] + " " + words[1] + " " + words[2]) < 25 and len(
                    words[3] + " " + words[4] + " " + words[5]) < 25:

                draw1.text(up_string, words[0] + " " + words[1] + " " + words[2], (255, 255, 255, 255), font=font)
                draw1.text(down_string, words[3] + " " + words[4] + " " + words[5], (255, 255, 255, 255), font=font)

            elif len(words) == 7 and len(words[0] + " " + words[1] + " " + words[2] + " " + words[3]) < 25 and len(
                    words[4] + " " + words[5] + " " + words[6]) < 25:

                draw1.text(up_string, words[0] + " " + words[1] + " " + words[2] + " " + words[3], (255, 255, 255, 255),
                           font=font)
                draw1.text(down_string, words[4] + " " + words[5] + " " + words[6], (255, 255, 255, 255), font=font)

            elif len(words) == 8 and len(words[0] + " " + words[1] + " " + words[2] + " " + words[3]) < 25 and len(
                    words[4] + " " + words[5] + " " + words[6] + " " + words[7]) < 25:

                draw1.text(up_string, words[0] + " " + words[1] + " " + words[2] + " " + words[3], (255, 255, 255, 255),
                           font=font)
                draw1.text(down_string, words[4] + " " + words[5] + " " + words[6] + words[7], (255, 255, 255, 255),
                           font=font)

            img2 = Image.open(img_name).convert('RGBA')
            img2 = img2.resize((1024, 1024))
            result2 = Image.alpha_composite(img2, img1)
            result2.save(save_path)


def get_first_frame():

    cap = cv2.VideoCapture(f'1.MOV')
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print('Error: Creating directory of data')
    ret, frame = cap.read()
    name = 'frame.png'
    cv2.imwrite(name, frame)
    cap.release()
    cv2.destroyAllWindows()
    return name


def hlwn(a):
    string = ""
    for i in a:
        if i == '':
            string = string + "⭐️\n"
        else:
            string = string + i + "\n"
    string = string + "⭐️\n"
    string = string + "#hollywoodnews #новостиголливуда "
    return string


def array_to_string(a):
    responde = ''
    for i in a:
        responde = responde + i
    return responde


def divide_to_words(s):
    symbols = [".", ",", ":", "!", "?", " ", '', '\n', "«", '»' '—', '-', '&']
    w = ''
    words = []
    for i in range(len(s)):

        if s[i] in symbols:
            if w != '':
                words.append(w)
                w = ''
            words.append(s[i])
        else:
            w = w + s[i]
    words.append(w)
    return words


def parse_string(s):
    s = s + "\n"
    k = ""
    a = []

    for i in s:
        if i != "":
            if i == "\n":
                a.append(k.strip())
                k = ""
            else:
                k = k + i
    return a