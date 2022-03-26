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
    menu.add(menu_item_location)
    bot.send_message(message.chat.id, welcome_message, reply_markup=menu)

@bot.message_handler(content_types=['location'])
def get_weather(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    units = 'metric'
    language = 'ru'
    city, desc, temp = weather_map.get(longitude, latitude, units, language)
    data = f'Погода по вашему местоположению:\nГород: {city}\nТемпература: {temp} °C\n{desc}'
    bot.send_message(message.chat.id, data)

bot.polling(none_stop=True)