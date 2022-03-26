import requests
import config
from pyowm import OWM
from pyowm.utils.config import get_default_config





class OpenWeatherMap:
    __base_url = 'https://api.openweathermap.org/data/2.5/weather'


    @property
    def base_url(self):
        return OpenWeatherMap.__base_url

    # получение погоды по координатам
    @staticmethod
    def get_by_coord(longitute: float, latitude: float, units: str, language: str):
        try:
            data = requests.get(
                OpenWeatherMap.__base_url,
                params={
                    'lat': latitude,
                    'lon': longitute,
                    'units': units,
                    'lang': language,
                    'appid': config.weather_token
                }).json()
            city = data['name']
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            return city, description, round(temp)

        except Exception as err:
            return err

    # получение погоды по названию города
    @staticmethod
    def get_by_name(city: str, language: str):
        try:
            config_dict = get_default_config()
            config_dict['language'] = language

            owm = OWM(config.weather_token, config_dict)
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(city)
            weather = observation.weather
            temp = weather.temperature('celsius')['temp']
            description = weather.detailed_status
            return description, round(temp)

        except Exception as err:
            return err