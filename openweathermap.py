import requests
import config


class OpenWeatherMap:
    __base_url = 'https://api.openweathermap.org/data/2.5/weather'

    @property
    def base_url(self):
        return OpenWeatherMap.__base_url

    @staticmethod
    def get(longitute: float, latitude: float, units: str, language: str):
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
            return city, description, str(temp)
        except Exception as err:
            return err


