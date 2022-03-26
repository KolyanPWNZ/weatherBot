import telebot
import config
from openweathermap import OpenWeatherMap
from telebot import types


bot = telebot.TeleBot(config.telegram_token)
weather_map = OpenWeatherMap()

@bot.message_handler(commands=['start'])
def start(message):
    welcome_message = 'Привет! Это бот для определения погоды.'
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_item_location = types.KeyboardButton('Узнать погоду по геолокации', request_location=True)
    menu_item_city = types.KeyboardButton('Узнать погоду по названию города', )
    menu.add(menu_item_location, menu_item_city) #
    bot.send_message(message.chat.id, welcome_message, reply_markup=menu)

@bot.message_handler(content_types=['location'])
def get_weather_by_coord(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    units = 'metric'
    language = 'ru'
    city, desc, temp = weather_map.get_by_coord(longitude, latitude, units, language)
    print(type(message.chat.id))
    print_weather(message.chat.id, city, desc, temp)


# вывод сообщения о погоде
def print_weather(chat_id: int, city: str, desc: str, temp: int):
    data = f'Полученные данные по погоде:\nГород: {city}\nТемпература: {temp} °C\n{desc}'
    bot.send_message(chat_id, data)

@bot.message_handler(content_types=['text'])
def request_city_name(message):
    send = bot.send_message(message.chat.id, "Введите название города:")
    bot.register_next_step_handler(send, get_weather_by_name, get_weather_by_name)


def get_weather_by_name(message, info):
    city = message.text
    language = message.from_user.language_code
    desc, temp = weather_map.get_by_name(city, language)
    print_weather(message.chat.id, city, desc, temp)


bot.polling(none_stop=True)