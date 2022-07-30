import telebot
from telebot import types

import requests
from bs4 import BeautifulSoup

map_day = {}
map_sign = {}

dict_day = {'вчера': 'yesterday', 'сегодня': 'today', 'завтра': 'tomorrow', 'неделя': 'week', 'месяц': 'month'}
dict_sign = {'овен': 'aries', 'телец': 'taurus', 'близнецы': 'gemini', 'рак': 'cancer', 'лев': 'leo', 'дева': 'virgo', 'весы': 'libra',
             'скорпион': 'scorpio', 'стрелец': 'sagittarius', 'козерог': 'capricorn', 'водолей': 'aquarius', 'рыбы': 'pisces'}

bot = telebot.TeleBot("5543164096:AAFbIEzvcTigwOyja8yTH-04fG3jt7WeGdk")


@bot.message_handler(commands=['start'])
def chose_day(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bottom1 = types.KeyboardButton(text='вчера')
    bottom2 = types.KeyboardButton(text='сегодня')
    bottom3 = types.KeyboardButton(text='завтра')
    bottom4 = types.KeyboardButton(text='неделя')
    bottom5 = types.KeyboardButton(text='месяц')

    keyboard.row(bottom1, bottom2, bottom3, bottom4, bottom5)
    bot.send_message(message.chat.id, 'выберите день', reply_markup=keyboard, parse_mode='html')


@bot.message_handler(func=lambda
        message: message.text == 'сегодня' or message.text == 'завтра' or message.text == 'вчера' or message.text == 'неделя' or message.text == 'месяц')
def chose_sign(message):
    map_day[message.chat.id] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, one_time_keyboard=True)
    bottom1 = types.KeyboardButton(text='овен\n ♈')
    bottom2 = types.KeyboardButton(text='телец\n ♉')
    bottom3 = types.KeyboardButton(text='близнецы\n ♊')
    bottom4 = types.KeyboardButton(text='рак\n ♋')
    bottom5 = types.KeyboardButton(text='лев\n ♌')
    bottom6 = types.KeyboardButton(text='дева\n ♍')
    bottom7 = types.KeyboardButton(text='весы\n ♎')
    bottom8 = types.KeyboardButton(text='скорпион\n ♏')
    bottom9 = types.KeyboardButton(text='стрелец\n ♐')
    bottom10 = types.KeyboardButton(text='козерог\n ♑')
    bottom11 = types.KeyboardButton(text='водолей\n ♒')
    bottom12 = types.KeyboardButton(text='рыбы\n ♓')
    keyboard.row(bottom1, bottom2, bottom3, bottom4)
    keyboard.row(bottom5, bottom6, bottom7, bottom8)
    keyboard.row(bottom9, bottom10, bottom11, bottom12)
    bot.send_message(message.chat.id, 'выберите знак зодиака', reply_markup=keyboard, parse_mode='html')


@bot.message_handler(content_types='text')
def show_prediction(message):
    map_sign[message.chat.id] = message.text
    day = map_day[message.chat.id]
    sign = map_sign[message.chat.id][:-3]
    list_of_predictions = prediction(day, sign)
    list_of_marks = marks(day, sign)
    for mess in list_of_predictions:
        bot.send_message(message.chat.id, mess.text, parse_mode='html')
    for mark in list_of_marks:
        mess = f'{mark.text[0]} {mark.text[1:]}'
        bot.send_message(message.chat.id, mess, parse_mode='html')


def prediction(day, sign):
    r = requests.get(f"https://horo.mail.ru/prediction/{dict_sign[sign]}/{dict_day[day]}/")
    soup = BeautifulSoup(r.content, 'html.parser')
    list = soup.find_all('p')
    return list


def marks(day, sign):
    r = requests.get(f"https://horo.mail.ru/prediction/{dict_sign[sign]}/{dict_day[day]}/")
    soup = BeautifulSoup(r.content, 'html.parser')
    list = soup.find_all('div', 'p-score-day__item')
    return list[:-1]


if __name__ == '__main__':
    bot.infinity_polling()
